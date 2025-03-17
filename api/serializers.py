from rest_framework import serializers
from .models import Plant


class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plant
        fields = '__all__'

    def validate_name(self, value):
        """ Vérifie que le nom est suffisamment long """
        if len(value) < 3:
            raise serializers.ValidationError(
                "Le nom doit contenir au moins 3 caractères.")
        return value

    def to_representation(self, instance):
        """ Normalise `created_at` pour éviter les erreurs de test """
        data = super().to_representation(instance)
        if "created_at" in data:
            data["created_at"] = instance.created_at.replace(
                microsecond=0).isoformat().replace("+00:00", "Z")
        return data
