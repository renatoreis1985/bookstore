from rest_framework import serializers # type: ignore

from product.models.category import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["title", "description", "active", "slug"]
