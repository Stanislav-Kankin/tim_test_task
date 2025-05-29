from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'telegram_user_id', 'product_name', 'quantity', 'price', 'status'
        )
    list_filter = ('status', 'created_at')
    search_fields = ('product_name', 'delivery_info')
    readonly_fields = ('created_at',)

    fieldsets = (
        (None, {
            'fields': ('telegram_user_id', 'product_name', 'quantity', 'price')
        }),
        ('Доставка', {
            'fields': ('delivery_info', 'status', 'created_at')
        }),
    )
