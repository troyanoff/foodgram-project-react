from django_filters import rest_framework as filters

from recipes import models


class RecipeFilter(filters.FilterSet):

    is_favorited = filters.NumberFilter(method='is_favorited')
    is_in_shopping_cart = filters.NumberFilter(method='is_in_shopping_cart')

    class Meta:
        model = models.Recipe
        fields = ('tags__name', 'author__id',)

    def is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorite_recipe__user=self.request.user)
        return queryset

    def is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(favorite_recipe__user=self.request.user)
        return queryset
