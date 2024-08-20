from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    CreateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from core.api.models import Measurement, Alert, Device
from core.api.serializers import (
    MeasurementSerializer,
    MeasurementResumenSerializer,
    CreateMeasurementSerializer,
    MeasurementResumenGroupedSerializer,
    MeasurementHistorySerializer,
)
from core.api.services import MeasurementService
from core.emails import send_html_email
from core.users.models import CustomUser
from core.utils import split_string
from core.utils.consts import IS_TRUE
from core.utils.response import custom_response
from core.utils.mixins import OptionalPaginationMixin


class MeasurementCreateView(CreateAPIView):
    """
    Handle POST requests for measurement data.
    """

    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = [IsAuthenticated]


class MeasurementAPICreateView(CreateAPIView):
    serializer_class = CreateMeasurementSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        datetime_str = f"{data['date']} {data['time']}"
        datetime_obj = parse_datetime(datetime_str)

        measurements = MeasurementService.save_measurements(data, datetime_obj)
        exceeded_limits = MeasurementService.check_exceeded_limits(measurements)

        device = Device.objects.get(id=data["deviceId"])
        device.status = True
        device.save(update_fields=["status", "updated_at"])

        self.schedule_device_deactivation(device)

        if exceeded_limits:
            self.send_alerts_and_create_notifications(exceeded_limits)

        return custom_response("Guardado exitosamente", status.HTTP_201_CREATED)

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
    def create_email_message(emission_limit, gases):
        message = f"Se ha superado el límite de emisión '{emission_limit.name}' para los siguientes gases:\n"
        for gas_info in gases:
            message += f" * Gas: {gas_info['gas']}, Concentración registrada: {gas_info['value']}\n"
        return message

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

    def schedule_device_deactivation(self, device):
        pass


class MeasurementRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Handle GET, PUT, PATCH, and DELETE requests for a single measurement.
    """

    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = [IsAuthenticated]


class MeasurementHistoryView(OptionalPaginationMixin, ListAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        group_by = self.request.query_params.get("group_by")
        if group_by:
            return MeasurementResumenGroupedSerializer
        return MeasurementResumenSerializer

    def get_queryset(self):
        params = self.get_query_params()
        return MeasurementService.get_measurements(params)

    def get_query_params(self) -> dict:
        """
        Query Parameters:
        - brickyard_ids         (str): Filter measurements by brickyard IDs.
        - gas_types             (str): Filter measurements by gas type IDs.
        - device_id             (str): Filter measurements by device ID.
        - start_date            (str): Filter measurements from start date.
        - end_date              (str): Filter measurements until end date.
        - by_emission_limit_id  (str): Return all measurement equal or above this limit.
        - group_by              (str): Group measurements by 'minute', 'hour', or 'day'.
        - paginated             (bool): Return paginated results if true.
        - limit                 (int): Number of results returned.
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
            "by_emission_limit_id": query_params.get("by_emission_limit_id"),
            "group_by": query_params.get("group_by"),
            "paginated": query_params.get("paginated") in IS_TRUE,
            "limit": int(query_params.get("limit")) if query_params.get("limit") else None,
        }

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return self.paginate_if_needed(queryset)


class MeasurementsHistoryView(ListAPIView):
    serializer_class = MeasurementHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        device_id = self.kwargs["device_id"]
        return Measurement.objects.filter(sensor__device_id=device_id)
