from collections import defaultdict
from django.utils.dateparse import parse_datetime
from django.db import transaction
from django.db.models import Q, Avg, F, Window, Max, Min
from django.db.models.functions import Trunc, RowNumber, Round
from core.api.models import (
    Measurement,
    GasType,
    LimitHistory,
    Device,
    Brickyard,
    EmissionLimit,
    Alert,
)
from core.api.models.gas_type import CO_ID, NO2_ID, SO2_ID, PM25_ID, PM10_ID, TEMPERATURE_ID
from core.emails import send_html_email
from core.users.models import CustomUser
from core.utils import split_string
from core.utils.consts import IS_TRUE


class MeasurementService:
    VALID_ORDER_FIELDS = {
        "date": "date",
        "gas_type": "sensor__gas_type__abbreviation",
        "device_name": "sensor__device__name",
    }

    # Save
    @staticmethod
    def save_measurements(data, datetime_obj, device: Device):
        sensors = {sensor.gas_type_id: sensor for sensor in device.sensor_set.all()}
        gas_types = {
            "co": CO_ID,
            "no2": NO2_ID,
            "so2": SO2_ID,
            "pm25": PM25_ID,
            "pm10": PM10_ID,
            "temperature": TEMPERATURE_ID,
        }
        measurements = []

        with transaction.atomic():
            for gas_type_name, gas_type_id in gas_types.items():
                sensor = sensors.get(gas_type_id)
                new_measurement = Measurement(
                    value=data[gas_type_name], date=datetime_obj, sensor=sensor
                )

                if gas_type_name != "temperature":
                    measurements.append(new_measurement)

            Measurement.objects.bulk_create(measurements)
        return measurements

    @staticmethod
    def check_exceeded_limits(measurements, brickyard: Brickyard):
        exceeded_emission_limits = {}

        base_filter = Q(is_active=True)
        brickyard_filter = Q(brickyard=brickyard)
        management_filter = Q(management__brickyard=brickyard)
        institution_filter = Q(institution__isnull=False)

        emission_limits = EmissionLimit.objects.prefetch_related("limithistory_set").filter(
            base_filter & (brickyard_filter | management_filter | institution_filter)
        )

        for emission_limit in emission_limits:
            limit_histories = {
                limit.gas_type_id: limit for limit in emission_limit.limithistory_set.all()
            }
            for measurement in measurements:
                gas_type_id = measurement.sensor.gas_type_id
                gas_type_name = measurement.sensor.gas_type.name
                limit_history = limit_histories.get(gas_type_id)

                if limit_history and measurement.value > limit_history.max_limit:
                    if emission_limit not in exceeded_emission_limits:
                        exceeded_emission_limits[emission_limit] = []

                    exceeded_emission_limits[emission_limit].append(
                        {
                            "gas": gas_type_name,
                            "measurement": measurement,
                            "limit_history": limit_history,
                        }
                    )

        return exceeded_emission_limits

    @staticmethod
    def schedule_device_deactivation(device):
        pass

    @staticmethod
    def handle_alerts_and_notifications(exceeded_limits, brickyard):
        for emission_limit, gases in exceeded_limits.items():
            if not emission_limit.is_active and (
                emission_limit.email_alert or emission_limit.app_alert
            ):
                continue

            recipients_brickyard, recipients_institution = MeasurementService.get_recipients(
                emission_limit, brickyard
            )

            context = {"emission_limit": emission_limit, "gases": gases}
            message = MeasurementService.create_email_message(emission_limit, gases)

            MeasurementService.send_alerts(
                recipients_brickyard,
                emission_limit,
                f"Alerta de {emission_limit.name}",
                context,
                message,
            )
            MeasurementService.send_alerts(
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

        query_brickyard = Q()
        query_institution = Q()
        if emission_limit.institution:
            query_institution |= Q(institution=emission_limit.institution)
            if emission_limit.is_public:
                query_brickyard |= Q(brickyard=brickyard)
        elif emission_limit.management:
            query_institution |= Q(institution=emission_limit.management.institution)
            if emission_limit.is_public:
                query_brickyard |= Q(brickyard=emission_limit.management.brickyard)
        elif emission_limit.brickyard:
            query_brickyard |= Q(brickyard=emission_limit.brickyard)

        if query_brickyard:
            recipients_brickyard.update(CustomUser.objects.filter(query_brickyard))
        if query_institution:
            recipients_institution.update(CustomUser.objects.filter(query_institution))

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

    @staticmethod
    def get_query_params(request) -> dict:
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
        - order_by              (list): Order results by any field in the model.
        """

        query_params = request.query_params

        return {
            "brickyard_ids": split_string(query_params.get("brickyard_ids")),
            "gas_type_ids": (
                split_string(query_params.get("gas_types"))
                if query_params.get("gas_types")
                else None
            ),
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
            "order_by": (
                split_string(query_params.get("order_by"), conversion_type=str)
                if query_params.get("order_by")
                else None
            ),
        }

    # Get
    @staticmethod
    def get_measurements(params):
        gas_types = (
            GasType.objects.filter(id__in=params["gas_type_ids"])
            if params["gas_type_ids"]
            else GasType.objects.exclude(id=TEMPERATURE_ID)
        )

        date_filter = MeasurementService.build_date_filter(params["start_date"], params["end_date"])
        device_filter = Q(sensor__device_id=params["device_id"]) if params["device_id"] else Q()

        measurements = (
            Measurement.objects.filter(
                Q(sensor__device__brickyard_id__in=params["brickyard_ids"])
                & Q(sensor__gas_type__in=gas_types)
                & date_filter
                & device_filter
            )
            .select_related("sensor", "sensor__device", "sensor__gas_type")
            .only("id", "value", "date", "sensor__device__name", "sensor__gas_type__abbreviation")
        )

        if params["group_by"]:
            measurements = MeasurementService.group_measurements(measurements, params["group_by"])

        if params["by_emission_limit_id"]:
            measurements = MeasurementService.get_above_emission_limit(
                measurements, params["by_emission_limit_id"]
            )

        measurements = measurements.annotate(
            row_num=Window(expression=RowNumber(), order_by=F("date").desc())
        )

        if params["limit"]:
            measurements = measurements.filter(row_num__lte=params["limit"])

        if params["order_by"]:
            order_by_fields = []
            for field in params["order_by"]:
                order_by_field = MeasurementService.VALID_ORDER_FIELDS.get(field.lstrip("-"))
                if order_by_field:
                    if field.startswith("-"):
                        order_by_fields.append(f"-{order_by_field}")
                    else:
                        order_by_fields.append(order_by_field)
            if order_by_fields:
                measurements = measurements.order_by(*order_by_fields)

        return measurements

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
            .values(
                "sensor__device__name",
                "sensor__gas_type__abbreviation",
                "sensor__gas_type__id",
                "group_period",
            )
            .annotate(value=Round(Avg("value"), 3))
        )

        return measurements.annotate(date=F("group_period"))

    @staticmethod
    def get_above_emission_limit(measurements, emission_limit_id):
        limit_history = LimitHistory.objects.filter(emission_limit_id=emission_limit_id)

        if not limit_history.exists():
            return measurements.none()

        limit_filter = Q()
        for limit in limit_history:
            limit_filter |= Q(sensor__gas_type_id=limit.gas_type_id, value__gte=limit.max_limit)

        return measurements.filter(limit_filter).distinct()

    @staticmethod
    def get_measurements_grouped_by_gas(params):
        measurements = MeasurementService.get_measurements(params)

        grouped_data = defaultdict(
            lambda: {
                "gas_type": None,
                "gas_abbreviation": None,
                "measurements": defaultdict(dict),
                "avg": None,
                "max": None,
                "min": None,
            }
        )

        if params["device_id"]:
            device_filter = Q(id=params["device_id"])
        else:
            device_filter = Q(brickyard_id__in=params["brickyard_ids"])

        device_names = Device.objects.filter(device_filter).values_list("name", flat=True)

        for measurement in measurements:
            if params["group_by"]:
                gas_id = measurement["sensor__gas_type__id"]
                gas_abbreviation = measurement["sensor__gas_type__abbreviation"]
                device_name = measurement["sensor__device__name"]
                date = measurement["date"]
                value = measurement["value"]
            else:
                gas_id = measurement.sensor.gas_type_id
                gas_abbreviation = measurement.sensor.gas_type.abbreviation
                device_name = measurement.sensor.device.name
                date = measurement.date
                value = measurement.value

            grouped_data[gas_id]["gas_type"] = gas_id
            grouped_data[gas_id]["gas_abbreviation"] = gas_abbreviation
            grouped_data[gas_id]["measurements"][date][device_name] = value

        for gas_id, data in grouped_data.items():
            aggregated_data = measurements.filter(sensor__gas_type__id=gas_id).aggregate(
                avg_value=Avg("value"), max_value=Max("value"), min_value=Min("value")
            )

            grouped_data[gas_id]["avg"] = aggregated_data["avg_value"]
            grouped_data[gas_id]["max"] = aggregated_data["max_value"]
            grouped_data[gas_id]["min"] = aggregated_data["min_value"]

            for date, devices in data["measurements"].items():
                for device_name in device_names:
                    if device_name not in devices:
                        devices[device_name] = None

            data["measurements"] = [
                {"date": date, **devices} for date, devices in data["measurements"].items()
            ]

        return grouped_data.values()
