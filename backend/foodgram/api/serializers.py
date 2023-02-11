from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recipes import models

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователей."""

    is_subscribed = serializers.SerializerMethodField()

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

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return user in obj.following.all()


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    measurement_unit = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = models.Ingredient

    def get_measurement_unit(self, obj):
        return obj.measurement_unit.name


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""

    class Meta:
        fields = '__all__'
        model = models.Tag


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов."""

    author = UserSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True)

    class Meta:
        fields = '__all__'
        model = models.Recipe
        depth = 1

    # def create(self, validated_data):
        # ingredients = validated_data.pop('ingredients')
        # validated_data['author'] = self.context['request'].user
        # return validated_data
        # recipe = models.Recipe.objects.create(**validated_data)
        # for ingredient in ingredients:
        #     current_ingredient = get_object_or_404(
        #         models.Ingredient,
        #         id=ingredient['id']
        #     )
        #     models.IngrMUAmount.objects.create(
        #         recipe=recipe,
        #         ingredient=current_ingredient,
        #         amount=ingredient['amount']
        #     )
        # return recipe
