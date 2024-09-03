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
    MeasurementGroupedByGasSerializer,
)
from core.api.services import MeasurementService
from core.emails import send_html_email
from core.users.models import CustomUser
from core.utils.response import custom_response
from core.utils.mixins import OptionalPaginationMixin


class MeasurementCreateView(CreateAPIView):
    """Handle POST requests for measurement data."""

    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = [IsAuthenticated]


class MeasurementAPICreateView(CreateAPIView):
    """Handle POST requests where all measurements data is sent at once."""

    serializer_class = CreateMeasurementSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        device = (
            Device.objects.select_related("brickyard")
            .prefetch_related("sensor_set")
            .get(id=data["deviceId"])
        )
        datetime_obj = parse_datetime(f"{data['date']} {data['time']}")

        brickyard = device.brickyard

        measurements = MeasurementService.save_measurements(data, datetime_obj, device)
        exceeded_limits = MeasurementService.check_exceeded_limits(measurements, brickyard)

        device.status = True
        device.save(update_fields=["status", "updated_at"])

        self.schedule_device_deactivation(device)

        if exceeded_limits:
            self.handle_alerts_and_notifications(exceeded_limits, brickyard)

        return custom_response("Guardado exitosamente", status.HTTP_201_CREATED)

    def handle_alerts_and_notifications(self, exceeded_limits, brickyard):
        for emission_limit, gases in exceeded_limits.items():
            if not emission_limit.is_active and (
                emission_limit.email_alert or emission_limit.app_alert
            ):
                continue

            recipients_brickyard, recipients_institution = self.get_recipients(
                emission_limit, brickyard
            )

            context = {"emission_limit": emission_limit, "gases": gases}
            message = self.create_email_message(emission_limit, gases)

            self.send_alerts(
                recipients_brickyard,
                emission_limit,
                f"Alerta de {emission_limit.name}",
                context,
                message,
            )
            self.send_alerts(
                recipients_institution,
                emission_limit,
                f"Alerta en ladrillera {brickyard.name}",
                {**context, "brickyard": brickyard},
                message,
            )

    @staticmethod
    def get_recipients(emission_limit, brickyard):
        recipients_brickyard = set()
        recipients_institution = set()
        if emission_limit.institution:
            recipients_institution.update(
                CustomUser.objects.filter(institution=emission_limit.institution)
            )
            if emission_limit.is_public:
                recipients_brickyard.update(CustomUser.objects.filter(brickyard=brickyard))
        elif emission_limit.management:
            recipients_institution.update(
                CustomUser.objects.filter(institution=emission_limit.management.institution)
            )
            if emission_limit.is_public:
                recipients_brickyard.update(
                    CustomUser.objects.filter(brickyard=emission_limit.management.brickyard)
                )
        elif emission_limit.brickyard:
            recipients_brickyard.update(
                CustomUser.objects.filter(brickyard=emission_limit.brickyard)
            )

        return list(recipients_brickyard), list(recipients_institution)

    @staticmethod
    def create_email_message(emission_limit, gases):
        message = f"Se ha superado el límite de emisión '{emission_limit.name}' para los siguientes gases:\n"
        for gas in gases:
            message += (
                f" * Gas: {gas['gas']}. "
                f"Máximo permitido: {gas['limit_history'].max_limit}. "
                f"Concentración registrada: {gas['measurement'].value}\n"
            )
        return message

    @staticmethod
    def send_alerts(recipients, emission_limit, subject, context, message):
        for recipient in recipients:
            if emission_limit.email_alert:
                send_html_email(
                    subject,
                    recipient.email,
                    "emails/alerts/measurement_alert.html",
                    context,
                )
            if emission_limit.app_alert:
                Alert.objects.create(
                    name=subject,
                    short_description=f"Se superó el límite de emisión {emission_limit.name}",
                    description=message,
                    user=recipient,
                )

    def schedule_device_deactivation(self, device):
        pass


class MeasurementRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """Handle GET, PUT, PATCH, and DELETE requests for a single measurement."""

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
        params = MeasurementService.get_query_params(self.request)
        return MeasurementService.get_measurements(params)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return self.paginate_if_needed(queryset)


class MeasurementGroupedByGasView(OptionalPaginationMixin, ListAPIView):
    serializer_class = MeasurementGroupedByGasSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        params = MeasurementService.get_query_params(self.request)
        grouped_data = MeasurementService.get_measurements_grouped_by_gas(params)
        return grouped_data

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return self.paginate_if_needed(queryset)
