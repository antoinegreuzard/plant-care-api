from django.urls import path
from .views import PlantListCreateView, PlantDetailView, PlantPhotoUploadView

urlpatterns = [
    path(
        'plants/',
        PlantListCreateView.as_view(),
        name='plant-list'),
    path(
        'plants/<int:pk>/',
        PlantDetailView.as_view(),
        name='plant-detail'),
    path(
        'plants/<int:pk>/upload-photo/',
        PlantPhotoUploadView.as_view(),
        name='plant-upload-photo'),
]
