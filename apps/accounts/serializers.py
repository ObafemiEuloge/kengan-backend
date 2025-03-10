"""
Serializers pour l'application accounts.
"""
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import User, UserStats, UserRank, UserBadge

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Sérialiseur personnalisé de token qui ajoute les données utilisateur à la réponse
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Ajouter les données utilisateur à la réponse du token
        user = self.user
        data.update({
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'avatar': user.avatar.url if user.avatar else None,
                'level': user.level,
            }
        })
        
        return data


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Sérialiseur personnalisé pour le rafraîchissement de token
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        return data


class RegisterSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour l'inscription des utilisateurs
    """
    password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password')
        
    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": _("Les mots de passe ne correspondent pas.")})
        
        # Valider le mot de passe avec les validateurs de Django
        try:
            validate_password(attrs['password'])
        except ValidationError as e:
            raise serializers.ValidationError({"password": list(e.messages)})
            
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )
        
        user.set_password(validated_data['password'])
        user.save()
        
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le profil utilisateur
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'avatar', 'level', 'xp', 'xp_to_next_level', 'registration_date')
        read_only_fields = ('id', 'email', 'level', 'xp', 'xp_to_next_level', 'registration_date')


class UserStatsSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour les statistiques utilisateur
    """
    class Meta:
        model = UserStats
        fields = ('total_duels', 'wins', 'losses', 'win_rate', 'avg_score', 'best_category', 'total_earnings')
        read_only_fields = fields


class UserRankSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le rang utilisateur
    """
    class Meta:
        model = UserRank
        fields = ('position', 'tier', 'badge')
        read_only_fields = fields


class UserBadgeSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour les badges utilisateur
    """
    class Meta:
        model = UserBadge
        fields = ('name', 'description', 'image_url', 'unlocked_at')
        read_only_fields = fields
