from django.contrib import admin
from .models import (
    User,
    Category,
    Subcategory,
    Product,
    Cart,
    Order,
    BroadcastMessage
)
from django.utils.html import format_html
from django.conf import settings
import requests


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("telegram_id", "username", "first_name", "last_name", "is_subscribed", "is_admin")
    search_fields = ("telegram_id", "username", "first_name", "last_name")
    list_filter = ("is_subscribed", "is_admin")


class SubcategoryInline(admin.TabularInline):
    model = Subcategory
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("name",)
    inlines = [SubcategoryInline]


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category")
    search_fields = ("name",)
    list_filter = ("category",)
    inlines = [ProductInline]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "subcategory", "price")
    search_fields = ("name", "description")
    list_filter = ("subcategory",)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product_name", "quantity", "price")
    search_fields = ("user__telegram_id", "product_name")
    list_filter = ("user",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "product_name", "quantity", "price", "status")
    search_fields = ("user__telegram_id", "product_name")
    list_filter = ("status", "user")


@admin.register(BroadcastMessage)
class BroadcastMessageAdmin(admin.ModelAdmin):
    list_display = ("text", "created_at", "is_sent", "send_now_button")

    def send_now_button(self, obj):
        return format_html(
            '<a class="button" href="{}">Отправить сейчас</a>',
            f"/admin/orders/broadcastmessage/{obj.id}/send/"
        )
    send_now_button.short_description = "Отправка"
    send_now_button.allow_tags = True

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path('<int:message_id>/send/', self.admin_site.admin_view(self.send_now_view), name="broadcast_send_now"),
        ]
        return custom_urls + urls

    def send_now_view(self, request, message_id):
        from django.shortcuts import redirect, get_object_or_404
        message = get_object_or_404(BroadcastMessage, pk=message_id)
        from .models import User
        users = User.objects.all()

        for user in users:
            if user.telegram_id:
                try:
                    requests.post(
                        f"https://api.telegram.org/bot{settings.BOT_TOKEN}/sendMessage",
                        data={"chat_id": user.telegram_id, "text": message.text}
                    )
                except Exception as e:
                    print(f"Ошибка отправки пользователю {user.telegram_id}: {e}")

        message.is_sent = True
        message.save()
        self.message_user(request, "Рассылка отправлена.")
        return redirect("/admin/orders/broadcastmessage/")
