import base64

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from recipes import models

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    """Сериализатор для декодирования картинок."""

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


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
        if isinstance(user, AnonymousUser):
            return False
        following = models.Following.objects.filter(
            user=obj,
            author=user
        ).exists()
        return following


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания пользователей."""

    class Meta:
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        model = User


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов в рецепте."""

    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit',
        read_only=True
    )
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name', read_only=True)

    class Meta:
        fields = ('id', 'name', 'measurement_unit', 'amount')
        model = models.Amount


class IngredientListSerializer(serializers.ModelSerializer):
    """Сериализатор ингредиентов."""

    measurement_unit = serializers.CharField(
        source='measurement_unit.name',
        read_only=True
    )

    class Meta:
        fields = ('id', 'name', 'measurement_unit')
        model = models.Ingredient


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
        if isinstance(self.context['request'].user, AnonymousUser):
            return False
        return (
            models.FavoriteRecipe.objects.filter(
                user=self.context['request'].user,
                recipe=obj
            ).exists()
        )

    def get_is_in_shopping_cart(self, obj):
        if isinstance(self.context['request'].user, AnonymousUser):
            return False
        return (
            models.ShopRecipe.objects.filter(
                user=self.context['request'].user,
                recipe=obj
            ).exists()
        )


class RecipeWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи рецептов."""

    author = UserSerializer(
        read_only=True
    )
    ingredients = IngredientSerializer(many=True, required=False)
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        required=False,
        queryset=models.Tag.objects.all()
    )
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        fields = '__all__'
        model = models.Recipe

    def validate_author(self, value):
        if value != self.context['request'].user:
            raise serializers.ValidationError(
                'Нельзя редактировать чужие рецепты!'
            )
        return value

    def validate_ingredients(self, value):
        id_list = []
        for ingredient in value:
            id_list.append(ingredient['ingredient']['id'])
        if len(id_list) != len(set(id_list)):
            raise serializers.ValidationError(
                'Нельзя добавлять одинаковые ингредиенты!'
            )
        return value

    def _add_related(self, ingredients, tags, recipe):
        if ingredients:
            recipe.ingredients.clear()
            for ingredient in ingredients:
                current_ingredient = get_object_or_404(
                    models.Ingredient,
                    id=ingredient['ingredient']['id']
                )
                current_amount = models.Amount.objects.get_or_create(
                    ingredient=current_ingredient,
                    amount=ingredient['amount']
                )
                recipe.ingredients.add(current_amount[0].id)
        if tags:
            recipe.tags.clear()
            for tag in tags:
                current_tag = get_object_or_404(models.Tag, id=tag.id)
                models.RecipeTag.objects.create(
                    tag=current_tag,
                    recipe=recipe
                )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = models.Recipe.objects.create(**validated_data)
        self._add_related(ingredients, tags, recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        self._add_related(ingredients, tags, instance)
        return super().update(instance, validated_data)


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
        following = models.Following.objects.filter(
            user=obj,
            author=user
        ).exists()
        return following

    def get_recipes(self, obj):
        return RecipeSerializer(
            models.Recipe.objects.filter(author=obj),
            many=True
        ).data

    def get_recipes_count(self, obj):
        return models.Recipe.objects.filter(author=obj).count()


class TokenSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('email', 'password')
        model = User
