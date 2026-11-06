from django.contrib import admin

from .models import Category, Item


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ("name",)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ("title", "type", "category", "status", "owner", "created_at")
    list_filter = ("type", "status", "category")
    search_fields = ("title", "description", "location")
