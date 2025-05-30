from django.contrib import admin
from .models import (
    User,
    Category,
    Subcategory,
    Product,
    Cart,
    Order
)


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
