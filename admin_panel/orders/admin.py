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
import requests
import os


BOT_TOKEN = os.getenv("BOT_TOKEN")

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
    list_display = ["__str__", "is_sent"]
    readonly_fields = ["is_sent"]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not obj.is_sent:
            users = User.objects.values_list("telegram_id", flat=True)

            for user_id in users:
                payload = {
                    "chat_id": user_id,
                    "text": obj.text,
                    "parse_mode": "HTML"
                }

                if obj.image:
                    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
                    files = {"photo": obj.image.open("rb")}
                    data = {"chat_id": user_id, "caption": obj.text, "parse_mode": "HTML"}
                    try:
                        requests.post(url, data=data, files=files)
                    except Exception as e:
                        print(f"Ошибка отправки фото пользователю {user_id}: {e}")
                else:
                    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                    try:
                        requests.post(url, data=payload)
                    except Exception as e:
                        print(f"Ошибка отправки сообщения пользователю {user_id}: {e}")

            obj.is_sent = True
            obj.save()
