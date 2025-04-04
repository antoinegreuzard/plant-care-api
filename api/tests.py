from io import BytesIO

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .helpers import get_personalized_advice
from .models import Plant, PlantPhoto
from .serializers import PlantSerializer
from datetime import date, timedelta


class PlantModelTest(TestCase):
    """ Tests pour le modèle Plant """

    def setUp(self):
        self.plant = Plant.objects.create(
            name="Aloe Vera",
            variety="Barbadensis",
            plant_type="succulent",
            purchase_date=date(2023, 5, 20),
            location="Salon",
            description="Plante médicinale."
        )

    def test_plant_creation(self):
        """ Vérifie que l'objet plante est bien créé """
        self.assertEqual(self.plant.name, "Aloe Vera")
        self.assertEqual(self.plant.variety, "Barbadensis")
        self.assertEqual(self.plant.plant_type, "succulent")
        self.assertEqual(self.plant.purchase_date, date(2023, 5, 20))
        self.assertEqual(self.plant.location, "Salon")
        self.assertEqual(self.plant.description, "Plante médicinale.")

    def test_plant_str_representation(self):
        """ Vérifie la représentation en string """
        self.assertEqual(str(self.plant), "Aloe Vera")


class PlantSerializerTest(TestCase):
    """ Tests pour le serializer PlantSerializer """

    def setUp(self):
        self.plant = Plant.objects.create(
            name="Aloe Vera",
            variety="Barbadensis",
            plant_type="succulent",
            purchase_date=date(2023, 5, 20),
            location="Salon",
            description="Plante médicinale."
        )

    def test_serializer_valid_data(self):
        """ Vérifie que le serializer fonctionne avec des données valides """
        serializer = PlantSerializer(instance=self.plant)

        expected_created_at = self. \
            plant. \
            created_at. \
            replace(microsecond=0). \
            isoformat(). \
            replace("+00:00", "Z")
        actual_created_at = serializer.data["created_at"]

        self.assertEqual(actual_created_at, expected_created_at)

    def test_serializer_invalid_data(self):
        """ Vérifie que le serializer renvoie une erreur pour un nom court """
        invalid_data = {"name": "Te"}  # Nom trop court (<3 caractères)
        serializer = PlantSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)


class PlantAPITest(TestCase):
    """ Tests pour les vues API """

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        self.plant1 = Plant.objects.create(
            name="Ficus Lyrata",
            variety="Fiddle Leaf",
            plant_type="indoor",
            purchase_date=date(
                2023,
                3,
                10),
            location="Bureau",
            description="Arbre d'intérieur populaire.")

        self.plant2 = Plant.objects.create(
            name="Monstera Deliciosa",
            variety="Variegata",
            plant_type="indoor",
            purchase_date=date(
                2023,
                4,
                15),
            location="Salon",
            description="Plante tropicale.")

        self.list_url = reverse("plant-list")
        self.detail_url = reverse(
            "plant-detail",
            kwargs={
                "pk": self.plant1.id})

    def test_get_all_plants(self):
        """ Vérifie que la liste des plantes est retournée correctement """
        response = self.client.get(self.list_url)
        plants = Plant.objects.all()
        serializer = PlantSerializer(plants, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_create_plant(self):
        """ Vérifie que la création d'une plante fonctionne """
        data = {
            "name": "Sansevieria",
            "variety": "Laurentii",
            "plant_type": "indoor",
            "purchase_date": "2023-06-10",
            "location": "Chambre",
            "description": "Plante très résistante."
        }
        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_plant = Plant.objects.get(name="Sansevieria")
        self.assertEqual(created_plant.variety, "Laurentii")

    def test_get_single_plant(self):
        """ Vérifie qu'on peut récupérer une plante spécifique """
        response = self.client.get(self.detail_url)
        plant = Plant.objects.get(id=self.plant1.id)
        serializer = PlantSerializer(plant)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_plant(self):
        """ Vérifie que la mise à jour d'une plante fonctionne """
        updated_data = {
            "name": "Ficus Modifié",
            "variety": "Giant",
            "plant_type": "indoor",
            "purchase_date": "2023-03-10",
            "location": "Bureau",
            "description": "Plante d'intérieur imposante."
        }
        response = self.client.put(
            self.detail_url, updated_data, format="json")

        self.plant1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.plant1.name, "Ficus Modifié")

    def test_delete_plant(self):
        """ Vérifie que la suppression d'une plante fonctionne """
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Plant.objects.filter(id=self.plant1.id).exists())


class PlantURLTests(TestCase):
    """ Tests pour vérifier les routes """

    def test_urls_are_resolved(self):
        """ Vérifie que les routes sont bien configurées """
        list_url = reverse("plant-list")
        detail_url = reverse("plant-detail", kwargs={"pk": 1})

        self.assertEqual(list_url, "/api/plants/")
        self.assertEqual(detail_url, "/api/plants/1/")


class PersonalizedAdviceTest(TestCase):
    """ Teste la génération de conseils personnalisés """

    def setUp(self):
        self.plant = Plant.objects.create(
            name="Monstera",
            sunlight_level="medium",
            temperature=18,
            humidity_level="medium"
        )

    def test_generate_advice(self):
        """ Vérifie que les conseils générés sont corrects """
        advice = get_personalized_advice(self.plant)

        expected_advice = [
            "Votre plante a besoin de lumière indirecte, évitez le soleil.",
            "L'humidité est correcte, surveillez les signes de sécheresse."]

        for expected in expected_advice:
            self.assertIn(expected, advice)


class PlantPhotoTest(TestCase):
    """ Teste l’upload des photos de plantes """

    def setUp(self):
        self.client = APIClient()

        # 🔹 Créer un utilisateur et l'authentifier pour éviter l'erreur 401
        self.user = User.objects.create_user(
            username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        # 🔹 Créer une plante pour le test d'upload
        self.plant = Plant.objects.create(
            name="Monstera",
            sunlight_level="medium",
            temperature=18,
            humidity_level="medium"
        )

    def generate_photo_file(self):
        """ 🔹 Génère une image en mémoire pour l'upload """
        image = Image.new(
            'RGB', (100, 100), color='red')  # Génère une image rouge
        image_io = BytesIO()
        image.save(image_io, format='JPEG')
        image_io.seek(0)
        return SimpleUploadedFile(
            "test.jpg",
            image_io.read(),
            content_type="image/jpeg")

    def test_upload_photo(self):
        """ Vérifie que l’upload de photo fonctionne """
        url = reverse("plant-upload-photo", kwargs={"pk": self.plant.id})

        # 🔹 Utilisation d'une image générée en mémoire
        image = self.generate_photo_file()

        data = {"plant": self.plant.id, "image": image}
        response = self.client.post(url, data, format="multipart")

        # 🔹 Vérification de la réponse attendue
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(PlantPhoto.objects.filter(plant=self.plant).exists())
