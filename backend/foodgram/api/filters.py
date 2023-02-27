from django_filters import rest_framework as filters

from recipes import models


class RecipeFilter(filters.FilterSet):

    is_favorited = filters.BooleanFilter(method='is_favorited')
    is_in_shopping_cart = filters.BooleanFilter(method='is_in_shopping_cart')
    tags = filters.CharFilter(field_name='tags__slug', lookup_expr='icontains')
    author = filters.CharFilter(
        field_name='author__id', lookup_expr='icontains')

    class Meta:
        model = models.Recipe
        fields = ('tags', 'author',)

    def is_favorited(self, queryset, name, value):
        if value:
            return queryset.filter(favorite_recipe__user=self.request.user)
        return queryset

    def is_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(shopping__user=self.request.user)
        return queryset
