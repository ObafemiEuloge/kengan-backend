"""
URLs pour la partie utilisateur de l'application accounts.
"""
from django.urls import path
from .views import UserProfileView

urlpatterns = [
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]