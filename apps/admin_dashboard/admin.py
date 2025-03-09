"""
Configuration de l'admin pour l'application admin_dashboard.
"""
from django.contrib import admin
from .models import AdminLog, SystemSetting


class AdminLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'type', 'severity', 'user', 'action', 'ip_address')
    list_filter = ('type', 'severity')
    search_fields = ('user', 'action', 'details')
    date_hierarchy = 'timestamp'
    readonly_fields = ('timestamp',)


class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ('key', 'category', 'description')
    list_filter = ('category',)
    search_fields = ('key', 'description')


admin.site.register(AdminLog, AdminLogAdmin)
admin.site.register(SystemSetting, SystemSettingAdmin)
