from django.contrib.auth import get_user_model
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
        following = models.User.objects.filter(
            following__user=obj
        )
        return user in following


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    measurement_unit = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        model = models.Amount

    def get_measurement_unit(self, obj):
        return obj.ingredient.measurement_unit.name

    def get_id(self, obj):
        return obj.ingredient.id

    def get_name(self, obj):
        return obj.ingredient.name


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов."""

    class Meta:
        fields = '__all__'
        model = models.Tag


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор рецептов."""

    author = UserSerializer(read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        fields = '__all__'
        model = models.Recipe
        depth = 1

    def get_is_favorited(self, obj):
        return (
            models.FavoriteRecipe.objects.filter(
                user=self.context['request'].user,
                recipe=obj
            ).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        return (
            models.ShopRecipe.objects.filter(
                user=self.context['request'].user,
                recipe=obj
            ).exists()
        )


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи рецептов."""

    class Meta:
        fields = '__all__'
        model = models.Recipe


class ShoppingCartSerializer(serializers.ModelSerializer):
    """"Сериализатор корзины."""

    class Meta:
        fields = '__all__'
        model = models.ShopRecipe
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=models.ShopRecipe.objects.all(),
                fields=['user', 'recipe']
            )
        ]


class FavoritedSerializer(serializers.ModelSerializer):
    """"Сериализатор корзины."""

    class Meta:
        fields = '__all__'
        model = models.FavoriteRecipe
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=models.FavoriteRecipe.objects.all(),
                fields=['user', 'recipe']
            )
        ]


class FollowingSerializer(serializers.ModelSerializer):
    """"Сериализатор корзины."""

    class Meta:
        fields = '__all__'
        model = models.Following
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=models.Following.objects.all(),
                fields=['user', 'author']
            )
        ]

    def validate_author(self, value):
        if value == self.initial_data['user']:
            raise serializers.ValidationError(
                'Нельзя подписаться на самого себя!'
            )
        return value


class UserSubsrcibeSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя после подписки."""

    is_subscribed = serializers.SerializerMethodField()
    recipes = RecipeSerializer(read_only=True, many=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
        model = User

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        following = models.User.objects.filter(
            following__user=obj
        )
        return user in following

    def get_recipes(self, obj):
        return RecipeSerializer(
            models.Recipe.objects.filter(author=obj).all(),
            many=True
        ).data

    def get_recipes_count(self, obj):
        return models.Recipe.objects.filter(author=obj).count()
