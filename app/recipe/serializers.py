from rest_framework import serializers
from core.models import Recipe
from core.models import Tag
from core.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    """Ingredient Serializer"""

    class Meta:
        model = Ingredient
        fields = ['id', 'name']
        read_only_fields = ['id']

 
class TagSerializer(serializers.ModelSerializer):
    """Tag Serializer"""

    class Meta:
        model = Tag
        fields = ['id', 'name']
        read_only_fields = ['id']


class RecipeSerializer(serializers.ModelSerializer):
    """Recipe Serializer"""
    tags = TagSerializer(many=True, required=False)
    ingredients = IngredientSerializer(many=True, required=False)

    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'time_mins', 'price', 'link', 'tags',
            'ingredients',
            ]
        read_only_fields = ['id']

    def _get_or_create_tags(self, tags, recipe):
        auth_user = self.context['request'].user
        for tag in tags:
            tag_obj, created = Tag.objects.get_or_create(
                user=auth_user,
                **tag,
            )
            recipe.tags.add(tag_obj)

    def _get_or_create_ingredients(self, ingredients, recipe):
        auth_user = self.context['request'].user
        for ingredient in ingredients:
            ingredient_obj, create = Ingredient.objects.get_or_create(
                user=auth_user,
                **ingredient,
            )
            recipe.ingredients.add(ingredient_obj)

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        ingredients = validated_data.pop('ingredients', [])
        recipe = Recipe.objects.create(**validated_data)
        self._get_or_create_tags(tags, recipe)
        self._get_or_create_ingredients(ingredients, recipe)

        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        if tags is not None:
            instance.tags.clear()
            self._get_or_create_tags(tags, instance)

        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        instance.save()
        return instance


class RecipeDetailSerializer(RecipeSerializer):
    """Recipe Detail View Serializer"""

    class Meta(RecipeSerializer.Meta):
        fields = RecipeSerializer.Meta.fields + ['description']
