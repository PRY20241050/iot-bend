from django.db import transaction
from django.db.models import Q, Avg, F
from django.db.models.functions import Trunc
from django.core.mail import send_mail
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    CreateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from core.api.pagination import GenericPagination
from core.api.models import Status, Measurement, Sensor, GasType, LimitHistory, Alert
from core.api.models.gas_type import CO_ID, NO2_ID, SO2_ID, PM25_ID, PM10_ID, TEMPERATURE_ID
from core.api.serializers import (
    StatusSerializer,
    MeasurementSerializer,
    MeasurementPaginationSerializer,
    CreateMeasurementSerializer,
    MeasurementGroupedPeriodsSerializer,
)
from core.users.models import CustomUser
from core.utils import split_string
from core.utils.response import custom_response


class MeasurementCreateView(CreateAPIView):
    """
    Handle POST requests for measurement data.
    """

    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = [IsAuthenticated]


class MeasurementRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Handle GET, PUT, PATCH, and DELETE requests for a single measurement.
    """

    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = [IsAuthenticated]


class MeasurementBySensorView(ListAPIView):
    """
    Handle GET requests for measurement by sensor ID.
    """

    serializer_class = MeasurementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        sensor_id = self.kwargs["sensor_id"]
        return Measurement.objects.filter(sensor_id=sensor_id)


class MeasurementPaginatedListView(ListAPIView):
    pagination_class = GenericPagination
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        group_by = self.request.query_params.get("group_by")
        if group_by:
            return MeasurementGroupedPeriodsSerializer
        return MeasurementPaginationSerializer

    def get_queryset(self):
        params = self.get_query_params()

        if not params["brickyard_ids"]:
            return Measurement.objects.none()

        gas_types = (
            GasType.objects.filter(id__in=params["gas_type_ids"])
            if params["gas_type_ids"]
            else GasType.objects.exclude(id=TEMPERATURE_ID)
        )
        date_filter = self.build_date_filter(params["start_date"], params["end_date"])
        device_filter = Q(sensor__device_id=params["device_id"]) if params["device_id"] else Q()

        measurements = (
            Measurement.objects.filter(
                Q(sensor__device__brickyard_id__in=params["brickyard_ids"])
                & Q(sensor__gas_type__in=gas_types)
                & date_filter
                & device_filter
            )
            .select_related("sensor", "sensor__device", "sensor__gas_type")
            .only("id", "value", "date", "sensor__device__name", "sensor__gas_type__name")
            .order_by("-date")
        )

        if params["group_by"]:
            measurements = self.group_measurements(measurements, params["group_by"])

        return measurements

    def get_query_params(self) -> dict:
        """
        Query Parameters:
        - brickyard_ids (str): Filter measurements by brickyard IDs.
        - gas_types     (str): Filter measurements by gas type IDs.
        - device_id     (str): Filter measurements by device ID.
        - start_date    (str): Filter measurements from start date.
        - end_date      (str): Filter measurements until end date.
        - group_by      (str): Group measurements by 'minute', 'hour', or 'day'.
        """

        query_params = self.request.query_params

        return {
            "brickyard_ids": split_string(query_params.get("brickyard_ids")),
            "gas_type_ids": split_string(query_params.get("gas_types")),
            "device_id": query_params.get("device_id"),
            "start_date": (
                parse_datetime(query_params.get("start_date"))
                if query_params.get("start_date")
                else None
            ),
            "end_date": (
                parse_datetime(query_params.get("end_date"))
                if query_params.get("end_date")
                else None
            ),
            "group_by": query_params.get("group_by"),
        }

    @staticmethod
    def build_date_filter(start_date, end_date):
        if start_date and end_date:
            return Q(date__range=[start_date, end_date])
        elif start_date:
            return Q(date__gte=start_date)
        elif end_date:
            return Q(date__lte=end_date)
        return Q()

    @staticmethod
    def group_measurements(measurements, group_by):
        if group_by not in ["minute", "hour", "day"]:
            raise ValueError("Valor inválido para group_by. Usa 'minute', 'hour', o 'day'.")

        measurements = (
            measurements.annotate(group_period=Trunc("date", group_by))
            .values("sensor__device__name", "sensor__gas_type__abbreviation", "group_period")
            .annotate(value=Avg("value"))
            .order_by("-group_period")
        )
        return measurements.annotate(date=F("group_period"))


class MeasurementAPICreateView(CreateAPIView):
    serializer_class = CreateMeasurementSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        device_id = data["deviceId"]
        datetime_str = f"{data['date']} {data['time']}"
        datetime_obj = parse_datetime(datetime_str)

        gas_types = {
            "co": CO_ID,
            "no2": NO2_ID,
            "so2": SO2_ID,
            "pm25": PM25_ID,
            "pm10": PM10_ID,
        }

        exceeded_limits = {}

        with transaction.atomic():
            for gas, gas_id in gas_types.items():
                try:
                    sensor = Sensor.objects.select_related("device", "gas_type").get(
                        device_id=device_id, gas_type_id=gas_id
                    )
                    measurement = Measurement.objects.create(
                        value=data[gas], date=datetime_obj, sensor=sensor
                    )

                    limit_histories = LimitHistory.objects.select_related("emission_limit").filter(
                        gas_type_id=gas_id,
                        emission_limit__management__brickyard=sensor.device.brickyard,
                    )

                    for limit_history in limit_histories:
                        if measurement.value > limit_history.max_limit:
                            emission_limit = limit_history.emission_limit
                            if emission_limit not in exceeded_limits:
                                exceeded_limits[emission_limit] = []
                            exceeded_limits[emission_limit].append(
                                {
                                    "gas": gas,
                                    "value": measurement.value,
                                    "measurement": measurement,
                                    "limit_history": limit_history,
                                }
                            )

                except Sensor.DoesNotExist:
                    return Response(
                        {"error": f"No se encontró el sensor para el gas: {gas}"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            if "temperature" in data:
                try:
                    temperature_sensor = Sensor.objects.get(device_id=device_id, gas_type_id=6)
                    Measurement.objects.create(
                        value=data["temperature"],
                        date=datetime_obj,
                        sensor=temperature_sensor,
                    )
                except Sensor.DoesNotExist:
                    return Response(
                        {"error": "No se encontró el sensor para la temperatura"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

        self.send_alerts_and_create_notifications(exceeded_limits)

        return Response({"detail": "Guardado exitosamente"}, status=status.HTTP_201_CREATED)

    def send_alerts_and_create_notifications(self, exceeded_limits):
        for emission_limit, gases in exceeded_limits.items():
            recipients = self.get_recipients(emission_limit) if emission_limit.email_alert else []

            for recipient in recipients:
                subject = "Alerta de Límite de Emisión Excedido"
                message = self.create_email_message(emission_limit, gases)

                if emission_limit.email_alert:
                    send_mail(subject, message, "no-reply@tuservicio.com", [recipient.email])

                if emission_limit.app_alert:
                    Alert.objects.create(
                        name=f"Alerta de {emission_limit.name}",
                        description=message,
                        user=recipient,
                    )

    def get_recipients(self, emission_limit):
        recipients = set()
        if emission_limit.institution:
            users = CustomUser.objects.filter(institution=emission_limit.institution)
            recipients.update(users)
        if emission_limit.management:
            brickyard_users = CustomUser.objects.filter(
                brickyard=emission_limit.management.brickyard
            )
            institution_users = CustomUser.objects.filter(
                institution=emission_limit.management.institution
            )
            recipients.update([*brickyard_users, *institution_users])

        return list(recipients)

    def create_email_message(self, emission_limit, gases):
        message = f"Se ha superado el límite de emisión '{emission_limit.name}' para los siguientes gases:\n"
        for gas_info in gases:
            message += f" * Gas: {gas_info['gas']}, Concentración registrada: {gas_info['value']}\n"
        return message


class StatusListCreateView(ListAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class StatusRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
