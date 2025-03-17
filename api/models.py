from django.db import models


class Plant(models.Model):
    TYPE_CHOICES = [
        ('indoor', 'Plante d’intérieur'),
        ('outdoor', 'Plante d’extérieur'),
        ('succulent', 'Succulente'),
        ('flower', 'Fleur'),
        ('tree', 'Arbre'),
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

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Plante"
        verbose_name_plural = "Plantes"

    def __str__(self):
        return self.name
