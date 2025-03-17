from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from .models import Plant, PlantPhoto
from .serializers import PlantSerializer, PlantPhotoSerializer


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

class PlantPhotoUploadView(generics.CreateAPIView):
    queryset = PlantPhoto.objects.all()
    serializer_class = PlantPhotoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)