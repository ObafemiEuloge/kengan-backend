"""
Modèles pour l'application ranking.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User


class Season(models.Model):
    """Saison de classement"""
    name = models.CharField(max_length=100)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.name} ({self.start_date.strftime('%Y-%m-%d')} - {self.end_date.strftime('%Y-%m-%d')})"


class RankingPeriod(models.Model):
    """Période de classement (hebdomadaire, mensuelle, saisonnière)"""
    PERIOD_TYPES = [
        ('weekly', 'Hebdomadaire'),
        ('monthly', 'Mensuelle'),
        ('seasonal', 'Saisonnière'),
        ('all_time', 'Tous les temps'),
    ]
    
    type = models.CharField(max_length=20, choices=PERIOD_TYPES)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    season = models.ForeignKey(Season, on_delete=models.CASCADE, related_name='periods', null=True, blank=True)
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.get_type_display()} ({self.start_date.strftime('%Y-%m-%d')} - {self.end_date.strftime('%Y-%m-%d')})"


class Ranking(models.Model):
    """Classement d'un utilisateur pour une période donnée"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rankings')
    period = models.ForeignKey(RankingPeriod, on_delete=models.CASCADE, related_name='rankings')
    position = models.PositiveIntegerField()
    score = models.PositiveIntegerField()
    win_rate = models.FloatField()
    total_duels = models.PositiveIntegerField()
    
    class Meta:
        unique_together = ('user', 'period')
        ordering = ['position']
    
    def __str__(self):
        return f"{self.user.username} - #{self.position} ({self.period})"


class Reward(models.Model):
    """Récompense pour un rang spécifique à la fin d'une période"""
    period = models.ForeignKey(RankingPeriod, on_delete=models.CASCADE, related_name='rewards')
    min_position = models.PositiveIntegerField()
    max_position = models.PositiveIntegerField()
    reward_type = models.CharField(max_length=100)
    reward_value = models.JSONField()
    
    def __str__(self):
        if self.min_position == self.max_position:
            return f"Récompense pour #{self.min_position} ({self.period})"
        return f"Récompense pour #{self.min_position}-{self.max_position} ({self.period})"
