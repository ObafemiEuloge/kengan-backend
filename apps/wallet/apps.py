"""
Configuration de l'application wallet.
"""
from django.apps import AppConfig


class WalletConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.wallet'
    verbose_name = 'Gestion du portefeuille'

    def ready(self):
        import apps.wallet.signals
