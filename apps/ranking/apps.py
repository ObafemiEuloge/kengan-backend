"""
Configuration de l'application ranking.
"""
from django.apps import AppConfig


class RankingConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.ranking'
    verbose_name = 'Gestion du classement'
