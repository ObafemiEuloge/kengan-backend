"""
Configuration de l'admin pour l'application wallet.
"""
from django.contrib import admin
from .models import Balance, Transaction, PaymentMethod


class BalanceAdmin(admin.ModelAdmin):
    list_display = ('user', 'total', 'available', 'pending', 'locked', 'currency')
    search_fields = ('user__username', 'user__email')


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'amount', 'status', 'created_at', 'completed_at')
    list_filter = ('type', 'status')
    search_fields = ('user__username', 'reference', 'description')
    date_hierarchy = 'created_at'


class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ('user', 'type', 'name', 'is_default', 'created_at')
    list_filter = ('type', 'is_default')
    search_fields = ('user__username', 'name')


admin.site.register(Balance, BalanceAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(PaymentMethod, PaymentMethodAdmin)
