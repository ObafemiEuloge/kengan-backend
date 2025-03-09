"""
Configuration de l'application admin_dashboard.
"""
from django.apps import AppConfig


class AdminDashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.admin_dashboard'
    verbose_name = 'Tableau de bord admin'
