from rest_framework import serializers

from .models import Plant, PlantPhoto
from .helpers import get_personalized_advice


class PlantSerializer(serializers.ModelSerializer):
    next_watering = serializers.SerializerMethodField()
    next_fertilizing = serializers.SerializerMethodField()
    next_repotting = serializers.SerializerMethodField()
    next_pruning = serializers.SerializerMethodField()
    advice = serializers.SerializerMethodField()

    class Meta:
        model = Plant
        fields = [
            'id', 'name', 'variety', 'plant_type', 'purchase_date',
            'location', 'description', 'created_at', 'watering_frequency',
            'fertilizing_frequency', 'repotting_frequency', 'pruning_frequency',
            'last_watering', 'last_fertilizing', 'last_repotting', 'last_pruning',
            'sunlight_level', 'temperature', 'humidity_level', 'next_watering',
            'next_fertilizing', 'next_repotting', 'next_pruning', 'advice'
        ]

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    def get_next_watering(self, obj):
        return obj.next_watering()

    def get_next_fertilizing(self, obj):
        return obj.next_fertilizing()

    def get_next_repotting(self, obj):
        return obj.next_repotting()

    def get_next_pruning(self, obj):
        return obj.next_pruning()

    def validate_name(self, value):
        """ Vérifie que le nom est suffisamment long """
        if len(value) < 3:
            raise serializers.ValidationError(
                "Le nom doit contenir au moins 3 caractères.")
        return value

    def get_advice(self, obj):
        return get_personalized_advice(obj)

    def to_representation(self, instance):
        """ Normalise `created_at` pour éviter les erreurs de test """
        data = super().to_representation(instance)
        if "created_at" in data:
            data["created_at"] = instance.created_at.replace(
                microsecond=0).isoformat().replace("+00:00", "Z")
        return data


class PlantPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlantPhoto
        fields = '__all__'
        read_only_fields = ['uploaded_at']

    def create(self, validated_data):
        """ Ajoute la plante automatiquement depuis la requête """
        plant_id = self.context['view'].kwargs.get('pk')
        validated_data['plant'] = Plant.objects.get(pk=plant_id)
        return super().create(validated_data)
