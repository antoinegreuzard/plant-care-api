from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import Plant, PlantPhoto
from .serializers import PlantSerializer, PlantPhotoSerializer


class PlantPagination(PageNumberPagination):
    page_size = 5


class PlantListCreateView(generics.ListCreateAPIView):
    serializer_class = PlantSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PlantPagination

    def get_queryset(self):
        # Restreint les plantes à l'utilisateur connecté s'il est authentifié
        if self.request.user.is_authenticated:
            return Plant.objects.filter(user=self.request.user).order_by('-created_at')
        return Plant.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PlantDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PlantSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        # Garantit que seuls les propriétaires puissent accéder/modifier
        return Plant.objects.filter(user=self.request.user)


class PlantPhotoUploadView(generics.CreateAPIView):
    serializer_class = PlantPhotoSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        plant_id = self.kwargs.get('pk')
        try:
            plant = Plant.objects.get(pk=plant_id, user=self.request.user)
        except Plant.DoesNotExist:
            raise PermissionDenied("Vous ne pouvez pas ajouter de photo à cette plante.")

        serializer.save(plant=plant)


class PlantPhotosListView(generics.ListAPIView):
    serializer_class = PlantPhotoSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        plant_id = self.kwargs['pk']
        return PlantPhoto.objects.filter(
            plant__id=plant_id,
            plant__user=self.request.user
        ).order_by('-uploaded_at')
