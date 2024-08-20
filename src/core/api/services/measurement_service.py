from django.db import transaction
from django.db.models import Q, Avg, F
from django.db.models.functions import Trunc
from rest_framework import status
from core.api.models import Measurement, Sensor, GasType, LimitHistory
from core.api.models.gas_type import CO_ID, NO2_ID, SO2_ID, PM25_ID, PM10_ID, TEMPERATURE_ID
from core.utils.response import custom_response


class MeasurementService:

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
            .order_by("-date")
        )

        if params["group_by"]:
            measurements = MeasurementService.group_measurements(measurements, params["group_by"])

        if params["by_emission_limit_id"]:
            measurements = MeasurementService.get_above_emission_limit(
                measurements, params["by_emission_limit_id"]
            )

        if params["limit"]:
            measurements = measurements[: params["limit"]]

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
            .annotate(value=Avg("value"))
            .order_by("-group_period")
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

        return measurements.filter(limit_filter).distinct().order_by("-date")
