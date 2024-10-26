from django.urls import reverse
from rest_framework.test import APITestCase
from core.api.models import Alert
from django.contrib.auth import get_user_model

User = get_user_model()


class AlertListViewTests(APITestCase):
    def setUp(self):
        # Crear un usuario de prueba y varias alertas
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)
        Alert.objects.create(user=self.user, is_read=False)
        Alert.objects.create(user=self.user, is_read=True)

    def test_get_queryset_filters_by_user(self):
        # Prueba que `get_queryset` filtra alertas por usuario
        url = reverse("my-alert-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 2)  # Debe retornar 2 alertas

    def test_unread_count_in_response(self):
        # Verificar que `unread_count` está en la respuesta y es correcto
        url = reverse("my-alert-list")
        response = self.client.get(url)
        unread_count = Alert.objects.filter(user=self.user, is_read=False).count()
        self.assertEqual(response.data["unread_count"], unread_count)


class AlertRetrieveUpdateDestroyViewTests(APITestCase):
    def setUp(self):
        # Crear usuario y alerta
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)
        self.alert = Alert.objects.create(user=self.user, is_read=False)

    def test_retrieve_alert(self):
        # Verificar que se puede recuperar la alerta correctamente
        url = reverse("alert-detail", kwargs={"pk": self.alert.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.alert.id)

    def test_update_alert(self):
        # Probar que se puede actualizar el campo `is_read` de la alerta
        url = reverse("alert-detail", kwargs={"pk": self.alert.pk})
        response = self.client.patch(url, {"is_read": True})
        self.alert.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.alert.is_read)

    def test_delete_alert(self):
        # Probar que se puede eliminar la alerta
        url = reverse("alert-detail", kwargs={"pk": self.alert.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Alert.objects.filter(pk=self.alert.pk).exists())


class AlertMarkAsReadViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.client.force_authenticate(user=self.user)
        self.alert1 = Alert.objects.create(user=self.user, is_read=False)
        self.alert2 = Alert.objects.create(user=self.user, is_read=False)

    def test_mark_all_alerts_as_read(self):
        # Probar que todas las alertas se marcan como leídas
        url = reverse("alert-mark-as-read") + "?mark_all=true"
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Alert.objects.filter(user=self.user, is_read=True).count(), 2)

    def test_mark_single_alert_as_read(self):
        # Probar que solo una alerta específica se marca como leída
        url = reverse("alert-mark-as-read") + f"?id={self.alert1.id}"
        response = self.client.post(url)
        self.alert1.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.alert1.is_read)
        self.assertFalse(self.alert2.is_read)  # Otra alerta sigue sin leer

    def test_mark_alert_not_found(self):
        # Probar que se devuelva un error cuando no se encuentra ninguna alerta
        url = reverse("alert-mark-as-read") + "?id=9999"  # ID que no existe
        response = self.client.post(url)
        self.assertEqual(response.status_code, 404)
