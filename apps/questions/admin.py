"""
Configuration de l'admin pour l'application questions.
"""
from django.contrib import admin
from .models import Category, Question, Option


class OptionInline(admin.TabularInline):
    model = Option
    extra = 4


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'category', 'difficulty', 'type', 'active', 'usage_count')
    list_filter = ('category', 'difficulty', 'type', 'active')
    search_fields = ('text',)
    inlines = [OptionInline]


admin.site.register(Category)
admin.site.register(Question, QuestionAdmin)
