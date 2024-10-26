from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from core.api.models import Brickyard
from core.users.models import CustomUser


class BrickyardBlackBoxTestCase(APITestCase):

    def setUp(self):
        # Crear un usuario para autenticación
        self.user = CustomUser.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        # Crear un Brickyard de prueba
        self.brickyard = Brickyard.objects.create(name="Test Brickyard", visible=True)

    def test_list_brickyards(self):
        # Prueba de listar Brickyards
        url = reverse("brickyard-list-create")  # Define la URL de la vista de lista
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_brickyard(self):
        # Prueba de creación de un nuevo Brickyard
        url = reverse("brickyard-list-create")
        data = {"name": "New Brickyard", "address": "x", "ruc": 12312312341, "visible": True}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Brickyard")

    def test_get_brickyard_detail(self):
        # Prueba de obtener detalles de un Brickyard
        url = reverse("brickyard-detail", args=[self.brickyard.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.brickyard.name)

    def test_update_brickyard(self):
        # Prueba de actualización de un Brickyard existente
        url = reverse("brickyard-detail", args=[self.brickyard.id])
        data = {"name": "Updated Brickyard"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Brickyard")

    def test_delete_brickyard(self):
        # Prueba de eliminación de un Brickyard
        url = reverse("brickyard-detail", args=[self.brickyard.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Brickyard.objects.filter(id=self.brickyard.id).exists())
