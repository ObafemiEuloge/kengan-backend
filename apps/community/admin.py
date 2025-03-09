"""
Configuration de l'admin pour l'application community.
"""
from django.contrib import admin
from .models import Friendship, DuelInvitation, Message


class FriendshipAdmin(admin.ModelAdmin):
    list_display = ('user', 'friend', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'friend__username')
    date_hierarchy = 'created_at'


class DuelInvitationAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'category', 'stake', 'status', 'created_at', 'expires_at')
    list_filter = ('status', 'category')
    search_fields = ('sender__username', 'recipient__username')
    date_hierarchy = 'created_at'


class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'content', 'read', 'created_at')
    list_filter = ('read',)
    search_fields = ('sender__username', 'recipient__username', 'content')
    date_hierarchy = 'created_at'


admin.site.register(Friendship, FriendshipAdmin)
admin.site.register(DuelInvitation, DuelInvitationAdmin)
admin.site.register(Message, MessageAdmin)
