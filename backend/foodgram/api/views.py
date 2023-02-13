from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken
)

from api import serializers, mixins
from recipes import models


class IngredientViewSet(mixins.RetrieveListViewSet):
    """Обработка операций с ингредиентами."""

    queryset = models.Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    pagination_class = (None)


class TagViewSet(mixins.RetrieveListViewSet):
    """Обработка операций с тегами."""

    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = (None)


class RecipeViewSet(viewsets.ModelViewSet):
    """Обработка операций с рецептами."""

    queryset = models.Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    permission_classes = (IsAuthenticated, )

    def _add_related(self, ingredients, tags, recipe):
        if ingredients != [{}]:
            recipe.ingredients.clear()
            for ingredient in ingredients:
                current_ingredient = get_object_or_404(
                    models.Ingredient,
                    id=ingredient['id']
                )
                current_amount = models.Amount.objects.get_or_create(
                    ingredient=current_ingredient,
                    amount=ingredient['amount']
                )
                recipe.ingredients.add(current_amount[0].id)
        if tags:
            recipe.tags.clear()
            for tag in tags:
                current_tag = get_object_or_404(models.Tag, id=tag)
                models.RecipeTag.objects.create(
                    tag=current_tag,
                    recipe=recipe
                )

    def create(self, request):
        """Обработка пост запроса."""
        ingredients = request.data.pop('ingredients')
        tags = request.data.pop('tags')
        request.data['author'] = self.request.user.id
        serializer = serializers.RecipeWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        recipe = models.Recipe.objects.get(id=serializer.data['id'])
        self._add_related(ingredients, tags, recipe)
        serializer = self.get_serializer(recipe)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        recipe = get_object_or_404(models.Recipe, id=self.kwargs.get('pk'))
        if recipe.author == self.request.user.id:
            return Response(
                **kwargs,
                status=status.HTTP_400_BAD_REQUEST)
        ingredients = request.data.pop('ingredients')
        tags = request.data.pop('tags')
        serializer = serializers.RecipeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(instance=recipe, validated_data=request.data)
        self._add_related(ingredients, tags, recipe)
        serializer = self.get_serializer(recipe)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    """Обработка операций с пользователями."""

    queryset = serializers.User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_object(self):
        if self.request.path == '/api/users/me/':
            return models.User.objects.get(id=self.request.user.id)
        return super().get_object()

    def update(self, request, *args, **kwargs):
        if self.request.path == '/api/users/set_password/':
            new_password = request.data.get('new_password')
            current_password = request.data.get('current_password')
            user = self.request.user
            if user.password == current_password:
                user.password = new_password
                user.save()
                serializer = self.get_serializer(user)
                return Response(serializer.data)
        return super().update(request, *args, **kwargs)

    @action(detail=False, methods=['get'], name='subscriptions')
    def subscriptions(self, request):
        user = request.user
        following = models.User.objects.filter(
            following__user=user
        )
        serializer = self.get_serializer(following, many=True)
        return Response(serializer.data)


class ShoppingViewSet(viewsets.ModelViewSet):
    """Обработка операций со списком покупок."""

    serializer_class = serializers.RecipeSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return None
        return super().get_serializer_class()

    def get(self):
        user = self.request.user
        return models.Recipe.objects.filter(shopping__user=user)

    def post(self, request):
        user = self.request.user
        recipe = get_object_or_404(models.Recipe, id=self.kwargs.get('id'))
        models.ShopRecipe.objects.create(user=user, recipe=recipe)
        serializer = serializers.RecipeSerializer(instance=recipe)
        return Response(serializer.data)

    def destroy(self, request):
        user = self.request.user
        recipe = get_object_or_404(models.Recipe, id=self.kwargs.get('id'))
        shopping_recipe = models.ShopRecipe.objects.get(
            user=user, recipe=recipe)
        shopping_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Создание JWT-токена."""

    email = request.data.get('email')
    password = request.data.get('password')

    if None not in (email, password):
        user = get_object_or_404(
            serializers.User,
            email=email,
            password=password
        )
        access = AccessToken.for_user(user)
        return Response({'auth_token': str(access), })
    return Response(request.data, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_token(request):
    """Создание JWT-токена."""
    for token in OutstandingToken.objects.filter(user=request.user):
        BlacklistedToken.objects.get_or_create(token=token)
    return Response(status=status.HTTP_204_NO_CONTENT)
