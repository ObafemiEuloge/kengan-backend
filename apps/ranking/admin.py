"""
Configuration de l'admin pour l'application ranking.
"""
from django.contrib import admin
from .models import Season, RankingPeriod, Ranking, Reward


class RankingPeriodInline(admin.TabularInline):
    model = RankingPeriod
    extra = 0


class RewardInline(admin.TabularInline):
    model = Reward
    extra = 0


class SeasonAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    inlines = [RankingPeriodInline]


class RankingPeriodAdmin(admin.ModelAdmin):
    list_display = ('type', 'start_date', 'end_date', 'season', 'is_active')
    list_filter = ('type', 'is_active', 'season')
    inlines = [RewardInline]


class RankingAdmin(admin.ModelAdmin):
    list_display = ('user', 'period', 'position', 'score', 'win_rate', 'total_duels')
    list_filter = ('period',)
    search_fields = ('user__username',)


admin.site.register(Season, SeasonAdmin)
admin.site.register(RankingPeriod, RankingPeriodAdmin)
admin.site.register(Ranking, RankingAdmin)
admin.site.register(Reward)
