from django.contrib import admin
from .models import Plant


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'plant_type', 'location', 'created_at')
    search_fields = ('name', 'variety', 'location')
    list_filter = ('plant_type', 'created_at')
    ordering = ('-created_at',)
