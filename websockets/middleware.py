"""
Middleware pour l'authentification WebSocket.
"""
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

@database_sync_to_async
def get_user(user_id):
    from apps.accounts.models import User
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()

class JWTAuthMiddleware(BaseMiddleware):
    """Middleware pour authentifier les utilisateurs via JWT dans les WebSockets"""
    
    async def __call__(self, scope, receive, send):
        # Extraire le token des paramètres de requête
        query_string = scope.get('query_string', b'').decode()
        query_params = dict(param.split('=') for param in query_string.split('&') if '=' in param)
        token = query_params.get('token')
        
        # Si pas de token dans les paramètres, chercher dans les headers
        if not token:
            headers = dict(scope.get('headers', []))
            auth_header = headers.get(b'authorization', b'').decode()
            
            if auth_header.startswith('Bearer '):
                token = auth_header[7:]
        
        # Authentifier l'utilisateur si un token est présent
        if token:
            try:
                payload = jwt.decode(
                    token,
                    settings.SECRET_KEY,
                    algorithms=['HS256']
                )
                user_id = payload.get('user_id')
                
                if user_id:
                    scope['user'] = await get_user(user_id)
                else:
                    scope['user'] = AnonymousUser()
            except (InvalidTokenError, ExpiredSignatureError):
                scope['user'] = AnonymousUser()
        else:
            scope['user'] = AnonymousUser()
        
        return await super().__call__(scope, receive, send)
