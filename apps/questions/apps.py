"""
Configuration de l'application questions.
"""
from django.apps import AppConfig


class QuestionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.questions'
    verbose_name = 'Gestion des questions'
