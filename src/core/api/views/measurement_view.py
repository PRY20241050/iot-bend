from django.db import transaction
from django.db.models import Q, Avg, F
from django.db.models.functions import Trunc
from django.utils.dateparse import parse_datetime
from rest_framework import status
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
from core.emails import send_html_email


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

        datetime_str = f"{data['date']} {data['time']}"
        datetime_obj = parse_datetime(datetime_str)

        measurements = self.save_measurements(data, datetime_obj)
        exceeded_limits = self.check_exceeded_limits(measurements)

        if exceeded_limits:
            self.send_alerts_and_create_notifications(exceeded_limits)

        return custom_response("Guardado exitosamente", status.HTTP_201_CREATED)

    def save_measurements(self, data, datetime_obj):
        device_id = data["deviceId"]
        gas_types = {
            "co": CO_ID,
            "no2": NO2_ID,
            "so2": SO2_ID,
            "pm25": PM25_ID,
            "pm10": PM10_ID,
        }
        measurements = []

        with transaction.atomic():
            for gas, gas_id in gas_types.items():
                sensor = self.get_sensor(device_id, gas, gas_id)
                measurement = Measurement.objects.create(
                    value=data[gas], date=datetime_obj, sensor=sensor
                )
                measurements.append(measurement)

            if "temperature" in data:
                self.save_temperature_measurement(device_id, data["temperature"], datetime_obj)

        return measurements

    def save_temperature_measurement(self, device_id, temperature, datetime_obj):
        sensor = self.get_sensor(device_id, "temperature", TEMPERATURE_ID)
        Measurement.objects.create(value=temperature, date=datetime_obj, sensor=sensor)

    @staticmethod
    def get_sensor(device_id, gas, gas_id):
        try:
            return Sensor.objects.select_related("device", "gas_type").get(
                device_id=device_id, gas_type_id=gas_id
            )
        except Sensor.DoesNotExist:
            raise custom_response(
                f"No se encontró el sensor para: {gas}", status.HTTP_400_BAD_REQUEST
            )

    @staticmethod
    def check_exceeded_limits(measurements):
        exceeded_limits = {}

        for measurement in measurements:
            gas = measurement.sensor.gas_type.name
            gas_id = measurement.sensor.gas_type_id

            limit_histories = LimitHistory.objects.select_related("emission_limit").filter(
                gas_type_id=gas_id,
                emission_limit__management__brickyard=measurement.sensor.device.brickyard,
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

        return exceeded_limits

    def send_alerts_and_create_notifications(self, exceeded_limits):
        for emission_limit, gases in exceeded_limits.items():
            recipients = self.get_recipients(emission_limit) if emission_limit.email_alert else []

            for recipient in recipients:
                if emission_limit.email_alert:
                    subject = "Alerta de Límite de Emisión Excedido"
                    send_html_email(
                        subject,
                        recipient.email,
                        "emails/alerts/measurement_alert.html",
                        {"emission_limit": emission_limit, "gases": gases},
                    )

                if emission_limit.app_alert:
                    message = self.create_email_message(emission_limit, gases)

                    Alert.objects.create(
                        name=f"Alerta de {emission_limit.name}",
                        description=message,
                        user=recipient,
                    )

    @staticmethod
    def get_recipients(emission_limit):
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

    @staticmethod
    def create_email_message(emission_limit, gases):
        message = f"Se ha superado el límite de emisión '{emission_limit.name}' para los siguientes gases:\n"
        for gas_info in gases:
            message += f" * Gas: {gas_info['gas']}, Concentración registrada: {gas_info['value']}\n"
        return message


class StatusListView(ListAPIView):
    """
    Handle GET requests for status data.
    """

    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class StatusRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Handle GET, PUT, PATCH, and DELETE requests for a single status.
    """

    queryset = Status.objects.all()
    serializer_class = StatusSerializer
