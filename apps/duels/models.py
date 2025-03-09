"""
Modèles pour l'application duels.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.accounts.models import User
from apps.questions.models import Question, Category, Option


class Duel(models.Model):
    """Duel entre deux joueurs"""
    STATUS_CHOICES = [
        ('waiting', 'En attente'),
        ('in_progress', 'En cours'),
        ('completed', 'Terminé'),
        ('cancelled', 'Annulé'),
    ]
    
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_duels')
    opponent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='joined_duels', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='duels')
    stake = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='won_duels', null=True, blank=True)
    
    def __str__(self):
        opponent_name = self.opponent.username if self.opponent else "Personne"
        return f"Duel: {self.creator.username} vs {opponent_name} ({self.get_status_display()})"


class DuelPlayer(models.Model):
    """Informations sur un joueur dans un duel"""
    duel = models.ForeignKey(Duel, on_delete=models.CASCADE, related_name='players')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ready = models.BooleanField(default=False)
    connected = models.BooleanField(default=True)
    score = models.PositiveIntegerField(default=0)
    last_activity = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('duel', 'user')
    
    def __str__(self):
        return f"{self.user.username} dans Duel #{self.duel.id}"


class DuelQuestion(models.Model):
    """Question associée à un duel spécifique"""
    duel = models.ForeignKey(Duel, on_delete=models.CASCADE, related_name='duel_questions')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    order = models.PositiveIntegerField()
    is_current = models.BooleanField(default=False)
    started_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ('duel', 'order')
        ordering = ['order']
    
    def __str__(self):
        return f"Question {self.order} - Duel #{self.duel.id}"


class DuelAnswer(models.Model):
    """Réponse d'un joueur à une question dans un duel"""
    duel_question = models.ForeignKey(DuelQuestion, on_delete=models.CASCADE, related_name='answers')
    player = models.ForeignKey(DuelPlayer, on_delete=models.CASCADE, related_name='answers')
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    is_correct = models.BooleanField()
    answer_time = models.FloatField()  # Temps en secondes
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('duel_question', 'player')
    
    def __str__(self):
        return f"Réponse de {self.player.user.username} - {self.is_correct}"


class DuelResult(models.Model):
    """Résultat final d'un duel"""
    duel = models.OneToOneField(Duel, on_delete=models.CASCADE, related_name='result')
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='+', null=True, blank=True)
    commission = models.PositiveIntegerField()
    completed_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        winner_name = self.winner.username if self.winner else "Match nul"
        return f"Résultat Duel #{self.duel.id} - Gagnant: {winner_name}"


class DuelPlayerResult(models.Model):
    """Résultat d'un joueur dans un duel"""
    duel_result = models.ForeignKey(DuelResult, on_delete=models.CASCADE, related_name='player_results')
    player = models.ForeignKey(DuelPlayer, on_delete=models.CASCADE)
    score = models.PositiveIntegerField()
    earnings = models.IntegerField()  # Peut être négatif
    
    def __str__(self):
        return f"{self.player.user.username}: {self.score} points, {self.earnings} FCFA"
