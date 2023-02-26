from django_filters import FilterSet

from recipes import models


class IngredientFilter(FilterSet):

    class Meta:
        model = models.Ingredient
        fields = {
            'name': ['startswith'],
        }
