from django.urls import path, include
from . import views

urlpatterns = [
    path('', include('core.users.urls')),
    path('brickyards/', views.BrickyardListCreateView.as_view(), name='brickyard-list-create'),
    path('brickyards/<int:pk>/', views.BrickyardRetrieveUpdateDestroyView.as_view(), name='brickyard-detail'),
    path('institution/', views.InstitutionListCreateView.as_view(), name='institution-list-create'),
    path('institution/<int:pk>/', views.InstitutionRetrieveUpdateDestroyView.as_view(), name='institution-detail'),
    path('institution/<int:institution_id>/brickyard/<int:brickyard_id>/', views.add_brickyard_to_institution, name='add-brickyard-to-institution'),
    path('institution/<int:institution_id>/add_brickyards/', views.add_multiple_brickyards_to_institution, name='add-brickyards-to-institution'),
]

