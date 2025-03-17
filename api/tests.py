from django.test import TestCase
from .models import Item


class ItemModelTest(TestCase):

    def setUp(self):
        self.item = Item.objects.create(name="Test Item", description="Ceci est un test")

    def test_item_creation(self):
        """ Vérifie que l'objet est bien créé """
        self.assertEqual(self.item.name, "Test Item")
        self.assertEqual(self.item.description, "Ceci est un test")

    def test_item_str_representation(self):
        """ Vérifie la représentation en string """
        self.assertEqual(str(self.item), "Test Item")
