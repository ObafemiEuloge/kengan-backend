"""
Configuration de l'application community.
"""
from django.apps import AppConfig


class CommunityConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.community'
    verbose_name = 'Gestion de la communauté'
