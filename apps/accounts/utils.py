from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from apps.notifications.models import NotificationTemplate

def send_welcome_email(user):
    """
    Envoyer un email de bienvenue au nouvel utilisateur
    """
    try:
        # Obtenir le template d'email
        template = NotificationTemplate.objects.get(code='welcome_email')
        
        # Remplacer les variables du template
        confirmation_link = f"{settings.FRONTEND_URL}/confirm-email?token={generate_confirmation_token(user)}"
        support_email = "support@kengan.com"
        
        subject = template.subject
        
        # Remplacer les variables dans le contenu
        content = template.content
        content = content.replace('{{username}}', user.username)
        content = content.replace('{{confirmation_link}}', confirmation_link)
        content = content.replace('{{support_email}}', support_email)
        
        # Envoyer l'email
        send_mail(
            subject,
            content,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        
        return True
    except Exception as e:
        print(f"Erreur d'envoi d'email de bienvenue: {e}")
        return False

def generate_confirmation_token(user):
    """
    Générer un token de confirmation pour la vérification d'email
    Ceci est une implémentation simple et devrait être remplacée par une méthode plus sécurisée en production
    """
    import jwt
    import datetime
    
    # Créer un token qui expire dans 24 heures
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    
    return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')