"""
Modèles pour l'application accounts.
"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """Modèle utilisateur étendu"""
    email = models.EmailField(_('email address'), unique=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    level = models.PositiveIntegerField(default=1)
    xp = models.PositiveIntegerField(default=0)
    xp_to_next_level = models.PositiveIntegerField(default=1000)
    registration_date = models.DateTimeField(auto_now_add=True)
    
    # Champs requis par Django
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        
    def __str__(self):
        return self.username


class UserStats(models.Model):
    """Statistiques de l'utilisateur"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='stats')
    total_duels = models.PositiveIntegerField(default=0)
    wins = models.PositiveIntegerField(default=0)
    losses = models.PositiveIntegerField(default=0)
    win_rate = models.FloatField(default=0.0)
    avg_score = models.FloatField(default=0.0)
    best_category = models.CharField(max_length=100, blank=True)
    total_earnings = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f"Stats de {self.user.username}"


class UserRank(models.Model):
    """Rang actuel de l'utilisateur"""
    RANK_CHOICES = [
        ('Genin', 'Genin'),
        ('Chunin', 'Chunin'),
        ('Jonin', 'Jonin'),
        ('Anbu', 'Anbu'),
        ('Kage', 'Kage'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='current_rank')
    position = models.PositiveIntegerField()
    tier = models.CharField(max_length=20, choices=RANK_CHOICES, default='Genin')
    badge = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.user.username} - {self.tier} (#{self.position})"


class UserBadge(models.Model):
    """Badge gagné par l'utilisateur"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    name = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.CharField(max_length=255)
    unlocked_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"
