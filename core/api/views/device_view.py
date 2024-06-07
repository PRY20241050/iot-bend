from django.http import JsonResponse, HttpResponse
from django.forms.models import model_to_dict
from core.api.models import Device
from core.api.serializers import DeviceSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

# @api_view(['GET', 'POST'])
# def api_home(request):
#     # Native Django ORM
#     # model_data = Device.objects.all()
#     # data = {}
#     # if model_data:
#     #     data = model_to_dict(model_data[0], fields=['name', 'description', 'status', 'battery_level', 'status_text'])

#     # Django REST Framework
#     instance = Device.objects.all()
#     data = {}
#     if instance:
#         serializer = DeviceSerializer(instance, many=True)
#         data = serializer.data

#     return Response(data)
