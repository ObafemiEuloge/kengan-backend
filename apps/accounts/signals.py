"""
Signaux pour l'application accounts.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserStats, UserRank


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Créer le profil de l'utilisateur à la création du compte"""
    if created:
        # Créer les statistiques
        UserStats.objects.create(user=instance)
        
        # Créer le rang initial
        UserRank.objects.create(
            user=instance,
            position=0,  # Sera mis à jour par le système de classement
            tier='Genin',
            badge='genin'
        )
