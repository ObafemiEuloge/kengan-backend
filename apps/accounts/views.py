from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from django.utils import timezone
from apps.admin_dashboard.models import AdminLog
from .serializers import (
    CustomTokenObtainPairSerializer, 
    CustomTokenRefreshSerializer,
    RegisterSerializer, 
    UserSerializer,
    UserStatsSerializer,
    UserRankSerializer,
    UserBadgeSerializer
)
from .models import User, UserStats, UserRank, UserBadge
from .throttling import LoginRateThrottle
from .utils import send_welcome_email

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Vue personnalisée de token qui utilise notre sérialiseur
    """
    serializer_class = CustomTokenObtainPairSerializer
    throttle_classes = [LoginRateThrottle]

    def post(self, request, *args, **kwargs):
        # Obtenir l'IP client pour la journalisation
        ip_address = self.get_client_ip(request)
        
        # Extraire l'email des données de la requête pour le suivi de connexion
        email = request.data.get('email', '')
        
        # Essayer d'authentifier
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == status.HTTP_200_OK:
            # Journaliser la connexion réussie
            self.log_login_attempt(email, True, ip_address)
        else:
            # Journaliser l'échec de connexion
            self.log_login_attempt(email, False, ip_address)
            
        return response
    
    def get_client_ip(self, request):
        """
        Obtenir l'adresse IP du client à partir de la requête
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def log_login_attempt(self, email, success, ip_address):
        """
        Journaliser la tentative de connexion dans les logs admin
        """
        action = 'Connexion réussie' if success else 'Échec de connexion'
        severity = 'info' if success else 'warning'
        
        # Créer une entrée dans les logs admin
        AdminLog.objects.create(
            type='auth',
            severity=severity,
            user=email,
            action=action,
            details=f"Tentative de connexion depuis l'adresse IP: {ip_address}",
            ip_address=ip_address
        )


class CustomTokenRefreshView(TokenRefreshView):
    """
    Vue personnalisée pour le rafraîchissement de token
    """
    serializer_class = CustomTokenRefreshSerializer


class RegisterView(APIView):
    """
    Vue API pour l'inscription des utilisateurs
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            # Générer les tokens
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token
            
            # Envoyer l'email de bienvenue
            send_welcome_email(user)
            
            # Retourner les tokens et les données utilisateur
            return Response({
                'refresh': str(refresh),
                'access': str(access),
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'avatar': user.avatar.url if user.avatar else None,
                    'level': user.level,
                }
            }, status=status.HTTP_201_CREATED)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    Vue API pour la déconnexion des utilisateurs
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            # Obtenir le refresh token
            refresh_token = request.data.get('refresh')
            
            if not refresh_token:
                return Response({"error": "Le refresh token est requis"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Créer l'objet token
            token = RefreshToken(refresh_token)
            
            # Blacklister le token
            token.blacklist()
            
            # Journaliser la déconnexion
            ip_address = self.get_client_ip(request)
            AdminLog.objects.create(
                type='auth',
                severity='info',
                user=request.user.email,
                action='Déconnexion',
                details=f"Déconnexion depuis l'adresse IP: {ip_address}",
                ip_address=ip_address
            )
            
            return Response({"success": "Déconnexion réussie"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def get_client_ip(self, request):
        """
        Obtenir l'adresse IP du client à partir de la requête
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class UserProfileView(APIView):
    """
    Vue API pour le profil utilisateur
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = request.user
        user_serializer = UserSerializer(user)
        stats_serializer = UserStatsSerializer(user.stats)
        rank_serializer = UserRankSerializer(user.current_rank)
        badges = UserBadge.objects.filter(user=user)
        badges_serializer = UserBadgeSerializer(badges, many=True)
        
        return Response({
            'profile': user_serializer.data,
            'stats': stats_serializer.data,
            'rank': rank_serializer.data,
            'badges': badges_serializer.data
        })