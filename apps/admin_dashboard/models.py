"""
Modèles pour l'application admin_dashboard.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User


class AdminLog(models.Model):
    """Journal d'activité des administrateurs"""
    TYPE_CHOICES = [
        ('auth', 'Authentification'),
        ('user', 'Utilisateur'),
        ('duel', 'Duel'),
        ('transaction', 'Transaction'),
        ('question', 'Question'),
        ('system', 'Système'),
    ]
    
    SEVERITY_CHOICES = [
        ('info', 'Information'),
        ('warning', 'Avertissement'),
        ('error', 'Erreur'),
        ('critical', 'Critique'),
    ]
    
    timestamp = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES, default='info')
    user = models.CharField(max_length=100)
    action = models.CharField(max_length=255)
    details = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.action} par {self.user} - {self.timestamp.strftime('%Y-%m-%d %H:%M')}"


class SystemSetting(models.Model):
    """Paramètres système"""
    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField()
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.key} ({self.category})"
