from rest_framework import viewsets

from api import serializers
from recipes import models


class IngredientViewSet(viewsets.ModelViewSet):
    """Обработка операций с ингредиентами."""

    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    pagination_class = (None)


class TagViewSet(viewsets.ModelViewSet):
    """Обработка операций с тегами."""

    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = (None)


class RecipeViewSet(viewsets.ModelViewSet):
    """Обработка операций с рецептами."""

    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
