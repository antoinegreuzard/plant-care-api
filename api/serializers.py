from rest_framework import serializers
from .models import Item


class ItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=255)

    class Meta:
        model = Item
        fields = '__all__'

    def validate_name(self, value):
        """ Empêche les noms trop courts """
        if len(value) < 3:
            raise serializers.ValidationError("Le nom doit contenir au moins 3 caractères.")
        return value
