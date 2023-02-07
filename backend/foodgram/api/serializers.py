from django.contrib.auth import get_user_model
from rest_framework import serializers

from api import relationals
from recipes import models

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""

    is_subscribed = relationals.FollowRelatedField(read_only=True)

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )
        model = User


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    class Meta:
        fields = '__all__'
        model = models.Ingredient


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""

    class Meta:
        fields = '__all__'
        model = models.Tag


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов."""

    ingredients = IngredientSerializer(read_only=True, many=True)
    tags = TagSerializer(read_only=True, many=True)
    author = UserSerializer()

    class Meta:
        fields = '__all__'
        model = models.Recipe
