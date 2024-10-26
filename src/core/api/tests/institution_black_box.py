from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from core.api.models import Institution
from core.users.models import CustomUser


class InstitutionBlackBoxTestCase(APITestCase):

    def setUp(self):
        # Crear un usuario para autenticación
        self.user = CustomUser.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        # Crear una institución de prueba
        self.institution = Institution.objects.create(name="Test Institution")

    def test_list_institutions(self):
        # Prueba de listar instituciones
        url = reverse("institution-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_institution(self):
        # Prueba de creación de una nueva institución
        url = reverse("institution-list-create")
        data = {"name": "New Institution", "address": "x"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "New Institution")

    def test_get_institution_detail(self):
        # Prueba de obtener detalles de una institución
        url = reverse("institution-detail", args=[self.institution.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.institution.name)

    def test_update_institution(self):
        # Prueba de actualización de una institución existente
        url = reverse("institution-detail", args=[self.institution.id])
        data = {"name": "Updated Institution"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Updated Institution")

    def test_delete_institution(self):
        # Prueba de eliminación de una institución
        url = reverse("institution-detail", args=[self.institution.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Institution.objects.filter(id=self.institution.id).exists())
