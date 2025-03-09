"""
Configuration de l'admin pour l'application accounts.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserStats, UserRank, UserBadge


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'level', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Informations', {'fields': ('avatar', 'level', 'xp', 'xp_to_next_level')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserStats)
admin.site.register(UserRank)
admin.site.register(UserBadge)
