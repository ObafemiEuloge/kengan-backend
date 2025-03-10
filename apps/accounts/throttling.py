from rest_framework.throttling import SimpleRateThrottle
from django.core.cache import cache

class LoginRateThrottle(SimpleRateThrottle):
    """
    Classe de limitation pour restreindre les tentatives de connexion par adresse IP
    """
    scope = 'login'
    
    def get_cache_key(self, request, view):
        # Obtenir les identifiants de connexion depuis les données de la requête
        email = request.data.get('email', '')
        
        # Utiliser à la fois l'email et l'adresse IP comme clé de cache
        ident = self.get_ident(request)
        
        # Retourner une clé de cache unique pour cet utilisateur et cette requête
        return f"login_attempt_{email}_{ident}"