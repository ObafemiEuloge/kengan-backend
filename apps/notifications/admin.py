"""
Configuration de l'admin pour l'application notifications.
"""
from django.contrib import admin
from .models import Notification, NotificationTemplate


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'type', 'is_read', 'created_at')
    list_filter = ('type', 'is_read')
    search_fields = ('user__username', 'title', 'message')
    date_hierarchy = 'created_at'


class NotificationTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'type', 'subject')
    list_filter = ('type',)
    search_fields = ('name', 'code', 'subject', 'content')


admin.site.register(Notification, NotificationAdmin)
admin.site.register(NotificationTemplate, NotificationTemplateAdmin)
