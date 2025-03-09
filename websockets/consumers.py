"""
Consommateurs pour les WebSockets.
"""
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

class DuelConsumer(AsyncWebsocketConsumer):
    """Consommateur WebSocket pour les duels"""
    
    async def connect(self):
        """Connexion au WebSocket"""
        self.user = self.scope['user']
        self.duel_id = self.scope['url_route']['kwargs']['duel_id']
        self.duel_group_name = f'duel_{self.duel_id}'
        
        # Rejoindre le groupe de duel
        await self.channel_layer.group_add(
            self.duel_group_name,
            self.channel_name
        )
        
        # Accepter la connexion WebSocket
        await self.accept()
    
    async def disconnect(self, close_code):
        """Déconnexion du WebSocket"""
        if hasattr(self, 'duel_group_name'):
            # Quitter le groupe
            await self.channel_layer.group_discard(
                self.duel_group_name,
                self.channel_name
            )
    
    async def receive(self, text_data):
        """Réception de données du client"""
        try:
            data = json.loads(text_data)
            # À implémenter
            pass
        except json.JSONDecodeError:
            pass


class NotificationConsumer(AsyncWebsocketConsumer):
    """Consommateur WebSocket pour les notifications"""
    
    async def connect(self):
        """Connexion au WebSocket"""
        self.user = self.scope['user']
        
        # Vérifier si l'utilisateur est authentifié
        if not self.user.is_authenticated:
            await self.close()
            return
        
        # Rejoindre le groupe de notifications de l'utilisateur
        self.notification_group_name = f'notifications_{self.user.id}'
        await self.channel_layer.group_add(
            self.notification_group_name,
            self.channel_name
        )
        
        # Accepter la connexion WebSocket
        await self.accept()
    
    async def disconnect(self, close_code):
        """Déconnexion du WebSocket"""
        if hasattr(self, 'notification_group_name'):
            # Quitter le groupe
            await self.channel_layer.group_discard(
                self.notification_group_name,
                self.channel_name
            )
