from rest_framework import serializers
from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    """Recipe Serializer"""

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_mins', 'price', 'link']
        read_only_fields = ['id']
