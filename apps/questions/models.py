"""
Modèles pour l'application questions.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    """Catégorie de questions"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = "Categories"


class Question(models.Model):
    """Question pour les duels"""
    TYPE_CHOICES = [
        ('text', 'Texte'),
        ('image', 'Image'),
        ('audio', 'Audio'),
        ('video', 'Vidéo'),
    ]
    
    DIFFICULTY_CHOICES = [
        ('easy', 'Facile'),
        ('medium', 'Moyen'),
        ('hard', 'Difficile'),
    ]
    
    text = models.CharField(max_length=500)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='text')
    image = models.ImageField(upload_to='questions/', blank=True, null=True)
    audio = models.FileField(upload_to='questions/audio/', blank=True, null=True)
    video = models.FileField(upload_to='questions/video/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='questions')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')
    time_limit = models.PositiveIntegerField(default=15)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    usage_count = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return self.text[:50]


class Option(models.Model):
    """Option de réponse pour une question"""
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.text} - {'Correcte' if self.is_correct else 'Incorrecte'}"
