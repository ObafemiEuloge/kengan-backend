"""
Configuration des routes WebSocket.
"""
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/duel/(?P<duel_id>\d+)/$', consumers.DuelConsumer.as_asgi()),
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
]
