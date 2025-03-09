"""
Configuration de l'admin pour l'application duels.
"""
from django.contrib import admin
from .models import (
    Duel, DuelPlayer, DuelQuestion, DuelAnswer, 
    DuelResult, DuelPlayerResult
)


class DuelPlayerInline(admin.TabularInline):
    model = DuelPlayer
    extra = 0


class DuelQuestionInline(admin.TabularInline):
    model = DuelQuestion
    extra = 0


class DuelAnswerInline(admin.TabularInline):
    model = DuelAnswer
    extra = 0


class DuelPlayerResultInline(admin.TabularInline):
    model = DuelPlayerResult
    extra = 0


class DuelAdmin(admin.ModelAdmin):
    list_display = ('id', 'creator', 'opponent', 'category', 'stake', 'status', 'created_at')
    list_filter = ('status', 'category')
    search_fields = ('creator__username', 'opponent__username')
    inlines = [DuelPlayerInline, DuelQuestionInline]


class DuelResultAdmin(admin.ModelAdmin):
    list_display = ('duel', 'winner', 'commission', 'completed_at')
    inlines = [DuelPlayerResultInline]


admin.site.register(Duel, DuelAdmin)
admin.site.register(DuelQuestion)
admin.site.register(DuelAnswer)
admin.site.register(DuelResult, DuelResultAdmin)
