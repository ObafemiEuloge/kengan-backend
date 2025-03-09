"""
Configuration de l'application duels.
"""
from django.apps import AppConfig


class DuelsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.duels'
    verbose_name = 'Gestion des duels'
