"""
Modèles pour l'application wallet.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User


class Balance(models.Model):
    """Solde de l'utilisateur"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='balance')
    total = models.IntegerField(default=0)
    available = models.IntegerField(default=0)
    pending = models.IntegerField(default=0)
    locked = models.IntegerField(default=0)
    currency = models.CharField(max_length=10, default='FCFA')
    
    def __str__(self):
        return f"Solde de {self.user.username}: {self.available} {self.currency}"


class Transaction(models.Model):
    """Transaction financière"""
    TYPE_CHOICES = [
        ('deposit', 'Dépôt'),
        ('withdrawal', 'Retrait'),
        ('duel_win', 'Gain de duel'),
        ('duel_loss', 'Perte de duel'),
        ('commission', 'Commission'),
        ('refund', 'Remboursement'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('completed', 'Terminée'),
        ('failed', 'Échouée'),
        ('cancelled', 'Annulée'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    amount = models.IntegerField()
    fee = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    description = models.CharField(max_length=255)
    reference = models.CharField(max_length=100, blank=True, null=True)
    duel = models.ForeignKey('duels.Duel', on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    
    def __str__(self):
        return f"{self.get_type_display()} de {self.amount} - {self.get_status_display()}"


class PaymentMethod(models.Model):
    """Méthode de paiement pour les dépôts/retraits"""
    TYPE_CHOICES = [
        ('card', 'Carte bancaire'),
        ('mobile_money', 'Mobile Money'),
        ('bank_transfer', 'Virement bancaire'),
        ('crypto', 'Cryptomonnaie'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payment_methods')
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    name = models.CharField(max_length=100)
    details = models.JSONField()
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()}) - {self.user.username}"
