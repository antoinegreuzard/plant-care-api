from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from .models import Plant
from .serializers import PlantSerializer


class PlantPagination(PageNumberPagination):
    page_size = 5


class PlantListCreateView(generics.ListCreateAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PlantPagination


class PlantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plant.objects.all()
    serializer_class = PlantSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
