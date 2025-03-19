from django.urls import path
from .views import (
    PlantListCreateView,
    PlantDetailView,
    PlantPhotoUploadView,
    PlantPhotosListView,
)

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

    path(
        'plants/<int:pk>/photos/',
        PlantPhotosListView.as_view(),
        name='plant-photos-list'),
]
