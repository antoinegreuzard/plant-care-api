from datetime import timedelta

from django.contrib.auth.models import User
from django.db import models


class Plant(models.Model):
    TYPE_CHOICES = [
        ('indoor', 'Plante d’intérieur'),
        ('outdoor', 'Plante d’extérieur'),
        ('succulent', 'Succulente'),
        ('flower', 'Fleur'),
        ('tree', 'Arbre'),
    ]

    SUNLIGHT_CHOICES = [
        ('low', 'Faible'),
        ('medium', 'Moyen'),
        ('high', 'Élevé'),
    ]

    HUMIDITY_CHOICES = [
        ('low', 'Sec'),
        ('medium', 'Moyen'),
        ('high', 'Humide'),
    ]

    name = models.CharField(max_length=255, unique=True, verbose_name="Nom")
    variety = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Variété")
    plant_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        verbose_name="Type de plante")
    purchase_date = models.DateField(
        blank=True, null=True, verbose_name="Date d’achat")
    location = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Emplacement")
    description = models.TextField(
        blank=True, null=True, verbose_name="Description")
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name="Date d’ajout")

    watering_frequency = models.IntegerField(
        default=7, verbose_name="Fréquence d’arrosage (jours)")
    fertilizing_frequency = models.IntegerField(
        default=30, verbose_name="Fréquence de fertilisation (jours)")
    repotting_frequency = models.IntegerField(
        default=365, verbose_name="Fréquence de rempotage (jours)")
    pruning_frequency = models.IntegerField(
        default=90, verbose_name="Fréquence de taille (jours)")

    last_watering = models.DateField(
        blank=True, null=True, verbose_name="Dernier arrosage")
    last_fertilizing = models.DateField(
        blank=True, null=True, verbose_name="Dernière fertilisation")
    last_repotting = models.DateField(
        blank=True, null=True, verbose_name="Dernier rempotage")
    last_pruning = models.DateField(
        blank=True, null=True, verbose_name="Dernière taille")

    sunlight_level = models.CharField(
        max_length=10,
        choices=SUNLIGHT_CHOICES,
        verbose_name="Ensoleillement",
        default="medium"
    )
    temperature = models.FloatField(
        verbose_name="Température (°C)",
        null=True,
        blank=True
    )
    humidity_level = models.CharField(
        max_length=10,
        choices=HUMIDITY_CHOICES,
        verbose_name="Humidité",
        default="medium"
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='plantes')

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Plante"
        verbose_name_plural = "Plantes"

    def __str__(self):
        return self.name

    def next_watering(self):
        """ Retourne la date du prochain arrosage """
        return self.last_watering + \
            timedelta(days=self.watering_frequency) \
            if self.last_watering \
            else None

    def next_fertilizing(self):
        """ Retourne la date de la prochaine fertilisation """
        return self.last_fertilizing + \
            timedelta(days=self.fertilizing_frequency) \
            if self.last_fertilizing \
            else None

    def next_repotting(self):
        """ Retourne la date du prochain rempotage """
        return self.last_repotting + \
            timedelta(days=self.repotting_frequency) \
            if self.last_repotting \
            else None

    def next_pruning(self):
        """ Retourne la date de la prochaine taille """
        return self.last_pruning + \
            timedelta(days=self.pruning_frequency) \
            if self.last_pruning \
            else None


class PlantPhoto(models.Model):
    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        related_name="photos")
    image = models.ImageField(upload_to="plant_photos/")
    caption = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Légende")
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de téléversement")

    class Meta:
        ordering = ["-uploaded_at"]
        verbose_name = "Photo de Plante"
        verbose_name_plural = "Photos de Plantes"

    def __str__(self):
        return (
            f"Photo de {self.plant.name}"
            f" - "
            f"{self.uploaded_at.strftime('%Y-%m-%d')}"
        )
