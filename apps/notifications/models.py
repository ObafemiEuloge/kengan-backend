"""
Modèles pour l'application notifications.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User


class Notification(models.Model):
    """Notification pour un utilisateur"""
    TYPE_CHOICES = [
        ('info', 'Information'),
        ('success', 'Succès'),
        ('warning', 'Avertissement'),
        ('error', 'Erreur'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=100)
    message = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='info')
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    data = models.JSONField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} pour {self.user.username} - {self.get_type_display()}"


class NotificationTemplate(models.Model):
    """Modèle de notification"""
    TYPE_CHOICES = [
        ('email', 'Email'),
        ('notification', 'Notification système'),
        ('sms', 'SMS'),
    ]
    
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    subject = models.CharField(max_length=200)
    content = models.TextField()
    variables = models.JSONField(help_text='Variables disponibles dans le template')
    
    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"
