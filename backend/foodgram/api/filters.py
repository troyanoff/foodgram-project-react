from django_filters import rest_framework as filters

from recipes import models


class RecipeFilter(filters.FilterSet):

    tags = filters.CharFilter(field_name='tags__slug')
    author = filters.NumberFilter(field_name='author__id')

    class Meta:
        model = models.Recipe
        fields = ('tags', 'author',)


class IngredientFilter(filters.FilterSet):

    class Meta:
        model = models.Ingredient
        fields = {
            'name': ['exact', 'icontains'],
        }
