"""
URLs pour l'application accounts.
"""
from django.urls import path
from rest_framework_simplejwt.views import TokenVerifyView
from .views import (
    CustomTokenObtainPairView, 
    CustomTokenRefreshView,
    RegisterView, 
    LogoutView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('refresh-token/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('verify-token/', TokenVerifyView.as_view(), name='token_verify'),
    path('logout/', LogoutView.as_view(), name='logout'),
]