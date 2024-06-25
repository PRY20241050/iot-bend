from django.db.models import Q, Avg, F
from django.db.models.functions import Trunc
from django.core.mail import send_mail
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from core.api.models import Status, Measurement, Sensor, GasType, LimitHistory
from core.api.serializers import (StatusSerializer, MeasurementSerializer,
                                  MeasurementPaginationSerializer, CreateMeasurementSerializer, MeasurementGroupedPeriodeSerializer)
from core.users.models import CustomUser


class StatusListCreateView(ListAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class StatusRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

# ------------------------


class MeasurementListView(ListCreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = [IsAuthenticated]


class MeasurementRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
    permission_classes = [IsAuthenticated]

# ------------------------


class MeasurementBySensorView(ListAPIView):
    serializer_class = MeasurementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        sensor_id = self.kwargs['sensor_id']
        return Measurement.objects.filter(sensor_id=sensor_id)


class MeasurementPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000


class MeasurementPaginatedListView(ListAPIView):
    pagination_class = MeasurementPagination
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        group_by = self.request.query_params.get('group_by')
        if group_by:
            return MeasurementGroupedPeriodeSerializer
        return MeasurementPaginationSerializer

    def get_queryset(self):
        brickyard_ids_str = self.request.query_params.get('brickyard_ids')
        gas_type_ids_str = self.request.query_params.get('gas_types')
        start_date_str = self.request.query_params.get('start_date')
        end_date_str = self.request.query_params.get('end_date')
        device_id = self.request.query_params.get('device_id')
        group_by = self.request.query_params.get('group_by')

        brickyard_ids = [int(id) for id in brickyard_ids_str.split(
            ',')] if brickyard_ids_str else []

        gas_type_ids = [int(id) for id in gas_type_ids_str.split(
            ',')] if gas_type_ids_str else []

        start_date = parse_datetime(start_date_str) if start_date_str else None
        end_date = parse_datetime(end_date_str) if end_date_str else None

        if not brickyard_ids:
            return Measurement.objects.none()

        if gas_type_ids:
            gas_types = GasType.objects.filter(id__in=gas_type_ids)
        else:
            gas_types = GasType.objects.all()
            print(gas_types)

        date_filter = Q()
        if start_date and end_date:
            date_filter = Q(date__range=[start_date, end_date])
        elif start_date:
            date_filter = Q(date__gte=start_date)
        elif end_date:
            date_filter = Q(date__lte=end_date)

        device_filter = Q()
        if device_id:
            device_filter = Q(sensor__device_id=device_id)

        measurements = Measurement.objects.filter(
            Q(sensor__device__brickyard_id__in=brickyard_ids) &
            Q(sensor__gas_type__in=gas_types) &
            date_filter &
            device_filter
        ).select_related('sensor', 'sensor__device', 'sensor__gas_type').only(
            'id', 'value', 'date', 'sensor__device__name', 'sensor__gas_type__name'
        ).order_by('-date')

        if group_by:
            if group_by not in ['minute', 'hour', 'day']:
                raise ValueError(
                    "Valor inválido para group_by. Usa 'minute', 'hour', o 'day'.")

            measurements = measurements.annotate(
                group_period=Trunc('date', group_by)
            ).values(
                'sensor__device__name', 'sensor__gas_type__abbreviation', 'group_period',
            ).annotate(
                value=Avg('value')
            ).order_by('-group_period')

            measurements = measurements.annotate(date=F('group_period'))

        return measurements


class MeasurementCreateView(CreateAPIView):
    serializer_class = CreateMeasurementSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        device_id = data['deviceId']
        datetime_str = f"{data['date']} {data['time']}"
        datetime_obj = parse_datetime(datetime_str)

        gas_types = {
            "co": 1,
            "no2": 2,
            "so2": 3,
            "pm25": 4,
            "pm10": 5,
        }

        exceeded_limits = {}

        for gas, gas_id in gas_types.items():
            try:
                sensor = Sensor.objects.get(
                    device_id=device_id, gas_type_id=gas_id)
                measurement = Measurement.objects.create(
                    value=data[gas],
                    date=datetime_obj,
                    sensor=sensor
                )

                # Verificar si el valor excede el límite
                limit_histories = LimitHistory.objects.filter(
                    gas_type_id=gas_id,
                    emission_limit__management__brickyard = sensor.device.brickyard
                )
                
                for limit_history in limit_histories:
                    print(".........")
                    if measurement.value > limit_history.max_limit:
                        emission_limit = limit_history.emission_limit
                        if emission_limit not in exceeded_limits:
                            exceeded_limits[emission_limit] = []
                        exceeded_limits[emission_limit].append({
                            "gas": gas,
                            "value": measurement.value,
                        })

            except Sensor.DoesNotExist:
                return Response({"error": f"No se encontró el sensor para el gas: {gas}"}, status=status.HTTP_400_BAD_REQUEST)

        if 'temperature' in data:
            try:
                temperature_sensor = Sensor.objects.get(
                    device_id=device_id, gas_type_id=6)
                Measurement.objects.create(
                    value=data['temperature'],
                    date=datetime_obj,
                    sensor=temperature_sensor
                )
            except Sensor.DoesNotExist:
                return Response({"error": "No se encontró el sensor para la temperatura"}, status=status.HTTP_400_BAD_REQUEST)

        self.send_alerts(exceeded_limits)

        return Response({"detail": "Guardado exitosamente"}, status=status.HTTP_201_CREATED)

    def send_alerts(self, exceeded_limits):
        for emission_limit, gases in exceeded_limits.items():
            if emission_limit.email_alert:
                recipients = self.get_recipients(emission_limit)
                if recipients:
                    print(recipients)
                    subject = "Alerta de emisión excedida"
                    message = self.create_email_message(emission_limit, gases)
                    send_mail(subject, message, 'no-reply@tuservicio.com', recipients)
            
    def get_recipients(self, emission_limit):
        recipients = set()
        if emission_limit.institution:
            users = CustomUser.objects.filter(institution=emission_limit.institution)
            recipients.update(user.email for user in users)
        if emission_limit.management:
            brickyard_users = CustomUser.objects.filter(brickyard=emission_limit.management.brickyard)
            institution_users = CustomUser.objects.filter(institution=emission_limit.management.institution)
            recipients.update(user.email for user in [*brickyard_users, *institution_users])
        return list(recipients)

    def create_email_message(self, emission_limit, gases):
        message = f"Se ha superado el límite de emisión '{emission_limit.name}':\n"
        for gas_info in gases:
            message += f" - Gas: {gas_info['gas']}, Valor: {gas_info['value']}\n"
        return message
