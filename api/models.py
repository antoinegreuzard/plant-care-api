from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Nom")
    description = models.TextField(
        blank=True, null=True, verbose_name="Description")
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Objet"
        verbose_name_plural = "Objets"

    def __str__(self):
        return self.name
