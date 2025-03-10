"""
Configuration de l'application accounts.
"""
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.accounts'
    verbose_name = 'Gestion des comptes'

    def ready(self):
        import apps.accounts.signals
