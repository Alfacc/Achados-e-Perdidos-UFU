from django.conf import settings
from django.utils import timezone
from rest_framework import serializers

from .models import Category, Item


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")


class ItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    owner_name = serializers.CharField(source="owner.name", read_only=True)

    class Meta:
        model = Item
        fields = (
            "id", "type", "title", "description", "category", "category_name",
            "location", "date_occurred", "photo", "status", "owner_name", "created_at",
        )
        read_only_fields = ("id", "status", "owner_name", "category_name", "created_at")

    def validate_date_occurred(self, value):
        if value > timezone.localdate():
            raise serializers.ValidationError("A data não pode estar no futuro.")
        return value

    def validate_photo(self, value):
        limit = settings.MAX_PHOTO_MB * 1024 * 1024
        if value and value.size > limit:
            raise serializers.ValidationError(f"A foto deve ter no máximo {settings.MAX_PHOTO_MB} MB.")
        return value
