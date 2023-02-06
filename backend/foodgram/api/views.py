from rest_framework import viewsets

from api import serializers
from recipes import models


class IngredientViewSet(viewsets.ModelViewSet):
    """Обработка операций с ингредиентами."""

    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
