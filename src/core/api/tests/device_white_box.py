from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from core.api.models import Device, Brickyard, GasType, Measurement
from core.users.models import CustomUser
from django.utils import timezone


class DeviceWhiteBoxTestCase(APITestCase):

    def setUp(self):
        # Crear un Brickyard de prueba
        self.brickyard = Brickyard.objects.create(
            name="Test Brickyard", address="Address", ruc=21318823123, visible=True
        )

        # Crear un usuario para autenticación
        self.user = CustomUser.objects.create(
            username="testuser", password="testpassword", brickyard=self.brickyard
        )
        self.client.force_authenticate(user=self.user)

        # Crear un dispositivo de prueba
        self.device = Device.objects.create(name="Test Device", brickyard=self.brickyard)

    def test_brickyard_id_filter(self):
        # Prueba del filtro `brickyard_id` en el queryset
        url = reverse("device-list-create") + f"?brickyard_id={self.brickyard.id}"
        response = self.client.get(url)
        # Comprueba que solo se devuelven dispositivos que coinciden con `brickyard_id=1`.
        for device in response.data:
            self.assertEqual(device["brickyard"], self.brickyard.id)

    def test_device_status_revalidation(self):
        # Prueba de revalidación de estado del dispositivo
        self.gas_type = GasType.objects.create(name="CO")
        self.device.sensor_set.create(gas_type=self.gas_type)

        # Simular una última medición anterior al tiempo de revalidación
        self.measurement = Measurement.objects.create(
            value=30,
            date=timezone.now() - timezone.timedelta(seconds=30),
            sensor=self.device.sensor_set.first(),
        )

        url = (
            reverse("device-list-create")
            + f"?brickyard_id={self.brickyard.id}"
            + "&revalidation_time_in_seconds=50"
        )
        response = self.client.get(url)
        device_data = response.data[0]
        self.assertIsNotNone(device_data)
        self.assertTrue(device_data["status"])

    def test_permission_required(self):
        # Prueba que se requiere autenticación
        self.client.force_authenticate(user=None)  # Desactiva autenticación
        url = reverse("device-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
