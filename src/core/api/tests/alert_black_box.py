from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from core.api.models import Alert
from core.users.models import CustomUser


class AlertAPITests(APITestCase):
    def setUp(self):
        # Crear un usuario para las pruebas
        self.user = CustomUser.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)
        self.alert_url = reverse("my-alert-list")

    def test_list_alerts(self):
        """Test para listar alertas"""
        Alert.objects.create(short_description="Test alert 1", user=self.user, is_read=False)
        Alert.objects.create(short_description="Test alert 2", user=self.user, is_read=True)

        response = self.client.get(self.alert_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_retrieve_alert(self):
        """Test para recuperar una alerta"""
        alert = Alert.objects.create(short_description="Test alert", user=self.user, is_read=False)
        url = reverse(
            "alert-detail", args=[alert.id]
        )  # Asegúrate de que el nombre de la URL sea correcto

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["short_description"], "Test alert")

    def test_mark_alert_as_read(self):
        """Test para marcar una alerta como leída"""
        alert = Alert.objects.create(short_description="Test alert", user=self.user, is_read=False)
        url = reverse("alert-mark-as-read") + f"?id={alert.id}"
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        alert.refresh_from_db()
        self.assertTrue(alert.is_read)

    def test_mark_all_alerts_as_read(self):
        """Test para marcar todas las alertas como leídas"""
        Alert.objects.create(short_description="Test alert 1", user=self.user, is_read=False)
        Alert.objects.create(short_description="Test alert 2", user=self.user, is_read=False)
        url = reverse("alert-mark-as-read") + "?mark_all=true"
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Alertas marcadas como leídas")
        alerts = Alert.objects.filter(user=self.user, is_read=True)
        self.assertEqual(alerts.count(), 2)

    def test_alert_not_found(self):
        """Test para marcar una alerta como leída que no existe"""
        url = reverse("alert-mark-as-read")
        response = self.client.post(url, {"id": 999})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["error"], "Alerta no encontrada")
