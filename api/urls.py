from django.urls import path
from .views import PlantListCreateView, PlantDetailView

urlpatterns = [
    path('plants/', PlantListCreateView.as_view(), name='plant-list'),
    path('plants/<int:pk>/', PlantDetailView.as_view(), name='plant-detail'),
]
