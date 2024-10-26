from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from core.api.models import Brickyard
from core.users.models import CustomUser


class BrickyardWhiteBoxTestCase(APITestCase):

    def setUp(self):
        # Crear un Brickyard de prueba
        self.brickyard = Brickyard.objects.create(name="Test Brickyard", visible=True)

        # Crear un usuario para autenticación
        self.user = CustomUser.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

    def test_visible_filter(self):
        # Prueba que solo los Brickyards visibles se devuelven en la lista
        Brickyard.objects.create(name="Hidden Brickyard", visible=False)
        url = reverse("brickyard-list-create")

        response = self.client.get(url)
        for brickyard in response.data:
            self.assertTrue(brickyard["visible"])

    def test_order_by_pk(self):
        # Prueba que los Brickyards se devuelven ordenados por 'pk'
        Brickyard.objects.create(name="Another Brickyard", visible=True)
        url = reverse("brickyard-list-create")
        response = self.client.get(url)
        pks = [brickyard["id"] for brickyard in response.data]
        self.assertEqual(pks, sorted(pks))

    def test_permission_required(self):
        # Prueba que se requiere autenticación
        self.client.force_authenticate(user=None)  # Desactiva autenticación
        url = reverse("brickyard-list-create")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
