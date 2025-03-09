"""
Signaux pour l'application wallet.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.accounts.models import User
from .models import Balance


@receiver(post_save, sender=User)
def create_user_balance(sender, instance, created, **kwargs):
    """Créer la balance de l'utilisateur à la création du compte"""
    if created:
        Balance.objects.create(
            user=instance,
            total=0,
            available=0,
            pending=0,
            locked=0,
            currency='FCFA'
        )
