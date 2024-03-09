from rest_framework import serializers
from core.models import Recipe
from core.models import Tag


class RecipeSerializer(serializers.ModelSerializer):
    """Recipe Serializer"""

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_mins', 'price', 'link']
        read_only_fields = ['id']


class RecipeDetailSerializer(RecipeSerializer):
    """Recipe Detail View Serializer"""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']


class TagSerializer(serializers.ModelSerializer):
    """Tag Serializer"""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']
