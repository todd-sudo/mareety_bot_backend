from django.contrib import admin

from . import models


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id", "title", "slug", "price", "category", "url",
    ]
    list_display_links = ["title", "slug", "price", "category"]
    search_fields = [
        "title", "slug",
    ]
    list_filter = ("category",)
    save_as = True
    save_on_top = True


@admin.register(models.CartProduct)
class CartProductAdmin(admin.ModelAdmin):
    list_display = [
        "id", "customer", "product", "qty", "final_price", "cart_id"
    ]
    list_display_links = ["customer", "product", "qty", "final_price"]
    save_as = True
    save_on_top = True


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "slug", "url"]
    list_display_links = ["name", "slug", "url"]
    search_fields = ["name", "slug"]
    save_as = True
    save_on_top = True


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "total_products", "final_price", "is_order"]
    list_display_links = ["customer", "total_products", "final_price"]
    list_editable = ["is_order"]
    save_as = True
    save_on_top = True


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = [
        "id", "tg_user_id", "first_name",
        "last_name", "phone", "address", "create_at", "lang"
    ]
    list_display_links = [
        "tg_user_id", "first_name",
        "last_name", "phone", "address", "create_at"
    ]
    search_fields = [
        "tg_user_id", "first_name", "last_name", "phone", "address"
    ]
    list_editable = ["lang"]

    save_as = True
    save_on_top = True


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "customer", "address", "status", "created_at"]
    list_display_links = ["id", "customer", "address", "created_at"]
    list_editable = ["status"]

    save_as = True
    save_on_top = True
