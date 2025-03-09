"""
Modèles pour l'application community.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User


class Friendship(models.Model):
    """Relation d'amitié entre deux utilisateurs"""
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('accepted', 'Acceptée'),
        ('declined', 'Refusée'),
        ('blocked', 'Bloquée'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_initiated')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friendships_received')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user', 'friend')
    
    def __str__(self):
        return f"{self.user.username} → {self.friend.username} ({self.get_status_display()})"


class DuelInvitation(models.Model):
    """Invitation à un duel"""
    STATUS_CHOICES = [
        ('pending', 'En attente'),
        ('accepted', 'Acceptée'),
        ('declined', 'Refusée'),
        ('expired', 'Expirée'),
    ]
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='duel_invitations_sent')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='duel_invitations_received')
    category = models.ForeignKey('questions.Category', on_delete=models.CASCADE, related_name='duel_invitations')
    stake = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    duel = models.ForeignKey('duels.Duel', on_delete=models.SET_NULL, null=True, blank=True, related_name='invitation')
    
    def __str__(self):
        return f"Invitation de {self.sender.username} à {self.recipient.username} - {self.get_status_display()}"


class Message(models.Model):
    """Message envoyé entre deux utilisateurs"""
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_sent')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_received')
    content = models.TextField()
    read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message de {self.sender.username} à {self.recipient.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
