from rest_framework import serializers

from recipes import models


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    class Meta:
        fields = '__all__'
        model = models.Ingredient
