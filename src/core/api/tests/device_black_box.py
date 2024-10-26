from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from core.api.models import Device, Brickyard
from core.users.models import CustomUser


class DeviceBlackBoxTestCase(APITestCase):

    def setUp(self):
        # Crear un Brickyard de prueba
        self.brickyard = Brickyard.objects.create(name="Test Brickyard", visible=True)

        # Crear un usuario para autenticación
        self.user = CustomUser.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        # Crear un dispositivo de prueba
        self.device = Device.objects.create(name="Test Device", brickyard=self.brickyard)

    def test_create_device(self):
        # Prueba de creación de un nuevo dispositivo
        url = reverse("device-list-create")
        data = {"name": "New Device", "brickyard": self.brickyard.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Device")

    def test_get_device_detail(self):
        # Prueba de obtener detalles de un dispositivo
        url = reverse("device-detail", args=[self.device.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.device.name)

    def test_update_device(self):
        # Prueba de actualización de un dispositivo existente
        url = reverse("device-detail", args=[self.device.id])
        data = {"name": "Updated Device"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Device")

    def test_delete_device(self):
        # Prueba de eliminación de un dispositivo
        url = reverse("device-detail", args=[self.device.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Device.objects.filter(id=self.device.id).exists())
