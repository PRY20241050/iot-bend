from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q
from core.api.models import Alert
from core.api.pagination import GenericPagination
from core.api.serializers import AlertSerializer
from core.permissions import IsOwner
from core.utils.response import custom_response
from core.utils.consts import IS_TRUE


class AlertListView(ListAPIView):
    """
    Handle GET and POST requests for alert data.
    """

    pagination_class = GenericPagination
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsOwner]

    def get_queryset(self):
        return Alert.objects.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        unread_count = queryset.aggregate(unread_count=Count("id", filter=Q(is_read=False)))

        response = super().list(request, *args, **kwargs)

        # Add unread count to response
        response.data["unread_count"] = unread_count["unread_count"]

        return response


class AlertRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    Handle GET, PUT, PATCH, and DELETE requests for a single alert.
    """

    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsOwner]


class AlertMarkAsReadView(CreateAPIView):
    """
    Handle POST requests for marking an alert as read.
    """

    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsOwner]

    def post(self, request, *args, **kwargs):
        query_params = self.request.query_params
        mark_all = query_params.get("mark_all") in IS_TRUE
        pk = query_params.get("id")

        if mark_all:
            alerts = Alert.objects.filter(user=request.user, is_read=False)
            for alert in alerts:
                alert.is_read = True
                alert.save()
            return custom_response("Alertas marcadas como leídas")

        if pk:
            alert = get_object_or_404(Alert, id=pk)
            alert.is_read = True
            alert.save()
            return custom_response("Alerta marcada como leída")

        return custom_response("Alerta no encontrada", status_code=404)
