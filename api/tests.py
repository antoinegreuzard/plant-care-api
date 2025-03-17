from django.contrib.auth.models import User

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Item
from .serializers import ItemSerializer


class ItemModelTest(TestCase):
    """ Tests pour le modèle Item """

    def setUp(self):
        self.item = Item.objects.create(
            name="Test Item", description="Ceci est un test")

    def test_item_creation(self):
        """ Vérifie que l'objet est bien créé """
        self.assertEqual(self.item.name, "Test Item")
        self.assertEqual(self.item.description, "Ceci est un test")

    def test_item_str_representation(self):
        """ Vérifie la représentation en string """
        self.assertEqual(str(self.item), "Test Item")


class ItemSerializerTest(TestCase):
    """ Tests pour le serializer ItemSerializer """

    def setUp(self):
        self.item = Item.objects.create(
            name="Test Item", description="Ceci est un test")

    def test_serializer_valid_data(self):
        """ Vérifie que le serializer fonctionne avec des données valides """
        serializer = ItemSerializer(instance=self.item)

        expected_created_at = self.item.created_at.replace(
            microsecond=0).isoformat().replace("+00:00", "Z")
        actual_created_at = serializer.data["created_at"]

        self.assertEqual(actual_created_at, expected_created_at)

    def test_serializer_invalid_data(self):
        """ Vérifie que le serializer renvoie une erreur """
        invalid_data = {"name": "Te"}  # Nom trop court (<3 caractères)
        serializer = ItemSerializer(data=invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("name", serializer.errors)


class ItemAPITest(TestCase):
    """ Tests pour les vues API """

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

        self.item1 = Item.objects.create(
            name="Item 1", description="Description 1")
        self.item2 = Item.objects.create(
            name="Item 2", description="Description 2")
        self.list_url = reverse("item-list")
        self.detail_url = reverse("item-detail", kwargs={"pk": self.item1.id})

    def test_get_all_items(self):
        """ Vérifie que la liste des items est retournée correctement """
        response = self.client.get(self.list_url)
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_create_item(self):
        """ Vérifie que la création d'un item fonctionne """
        data = {"name": "Nouvel Item", "description": "Nouvelle description"}
        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_item = Item.objects.get(name="Nouvel Item")
        self.assertEqual(created_item.name, "Nouvel Item")

    def test_get_single_item(self):
        """ Vérifie qu'on peut récupérer un item spécifique """
        response = self.client.get(self.detail_url)
        item = Item.objects.get(id=self.item1.id)
        serializer = ItemSerializer(item)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_update_item(self):
        """ Vérifie que la mise à jour d'un item fonctionne """
        updated_data = {
            "name": "Item modifié",
            "description": "Nouvelle description"}
        response = self.client.put(
            self.detail_url, updated_data, format="json")

        self.item1.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.item1.name, "Item modifié")

    def test_delete_item(self):
        """ Vérifie que la suppression d'un item fonctionne """
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Item.objects.filter(id=self.item1.id).exists())


class URLTests(TestCase):
    """ Tests pour vérifier les routes """

    def test_urls_are_resolved(self):
        """ Vérifie que les routes sont bien configurées """
        list_url = reverse("item-list")
        detail_url = reverse("item-detail", kwargs={"pk": 1})

        self.assertEqual(list_url, "/api/items/")
        self.assertEqual(detail_url, "/api/items/1/")
