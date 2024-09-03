from collections import defaultdict
from rest_framework.exceptions import NotFound
from django.utils.dateparse import parse_datetime
from django.db import transaction
from django.db.models import Q, Avg, F, Window, Max, Min
from django.db.models.functions import Trunc, RowNumber, Round
from core.api.models import Measurement, Sensor, GasType, LimitHistory, Device
from core.api.models.gas_type import CO_ID, NO2_ID, SO2_ID, PM25_ID, PM10_ID, TEMPERATURE_ID
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
    def save_measurements(data, datetime_obj):
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
                sensor = MeasurementService.get_sensor(device_id, gas, gas_id)
                measurement = Measurement.objects.create(
                    value=data[gas], date=datetime_obj, sensor=sensor
                )
                measurements.append(measurement)

            if "temperature" in data:
                MeasurementService.save_temperature_measurement(
                    device_id, data["temperature"], datetime_obj
                )

        return measurements

    @staticmethod
    def save_temperature_measurement(device_id, temperature, datetime_obj):
        sensor = MeasurementService.get_sensor(device_id, "temperature", TEMPERATURE_ID)
        Measurement.objects.create(value=temperature, date=datetime_obj, sensor=sensor)

    @staticmethod
    def get_sensor(device_id, gas, gas_id):
        try:
            return Sensor.objects.select_related("device", "gas_type").get(
                device_id=device_id, gas_type_id=gas_id
            )
        except Sensor.DoesNotExist:
            raise NotFound(f"No se encontró el sensor para: {gas}")

    @staticmethod
    def check_exceeded_limits(measurements):
        exceeded_limits = {}

        for measurement in measurements:
            gas_name = measurement.sensor.gas_type.name
            gas_id = measurement.sensor.gas_type_id
            brickyard_id = measurement.sensor.device.brickyard_id

            base_filter = Q(gas_type_id=gas_id, emission_limit__is_active=True)
            brickyard_filter = Q(emission_limit__brickyard_id=brickyard_id)
            management_filter = Q(emission_limit__management__brickyard_id=brickyard_id)
            institution_filter = Q(emission_limit__institution__isnull=False)

            limit_histories = LimitHistory.objects.select_related("emission_limit").filter(
                base_filter & (brickyard_filter | management_filter | institution_filter)
            )

            for limit_history in limit_histories:
                if measurement.value > limit_history.max_limit:
                    emission_limit = limit_history.emission_limit

                    if emission_limit not in exceeded_limits:
                        exceeded_limits[emission_limit] = []

                    exceeded_limits[emission_limit].append(
                        {
                            "gas": gas_name,
                            "measurement": measurement,
                            "limit_history": limit_history,
                        }
                    )

        return exceeded_limits

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
