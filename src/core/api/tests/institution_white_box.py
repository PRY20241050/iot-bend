from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from core.api.models import Institution
from core.users.models import CustomUser


class InstitutionWhiteBoxTestCase(APITestCase):

    def setUp(self):
        # Crear un usuario para autenticación
        self.user = CustomUser.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        # Crear una institución de prueba
        self.institution = Institution.objects.create(name="Test Institution")

    def test_permission_required(self):
        # Prueba que se requiere autenticación
        self.client.force_authenticate(user=None)
        url = reverse("institution-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_queryset_returned(self):
        # Verificar que la vista devuelve el queryset completo de Institution
        Institution.objects.create(name="Another Institution")
        url = reverse("institution-list-create")
        response = self.client.get(url)
        self.assertEqual(len(response.data), Institution.objects.count())
