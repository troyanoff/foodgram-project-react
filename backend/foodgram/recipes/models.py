from django.contrib.auth import get_user_model
from django.db import models
from foodgram.settings import MEASUREMENT_UNITS

User = get_user_model()


class Ingredient(models.Model):
    """Модель ингредиента."""

    name = models.CharField(max_length=100, verbose_name='Название')
    measurement_unit = models.CharField(
        max_length=10,
        choices=MEASUREMENT_UNITS,
        verbose_name='Единица измерения'
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Модель связи рецептов и ингредиента."""

    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='ing_rec',
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )
    amount = models.IntegerField(verbose_name='Количество')


class Tag(models.Model):
    """Модель тега."""

    name = models.CharField(max_length=20, verbose_name='Название')
    color = models.CharField(
        max_length=7,
        default='#ffffff',
        verbose_name='Цвет'
    )
    slug = models.SlugField(unique=True, verbose_name='Уникальное имя')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class RecipeTag(models.Model):
    """Модель связи рецептов и тегов."""

    recipe = recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    tag = models.ForeignKey(
        Tag,
        on_delete=models.SET_NULL,
        blank=True,
        null=True
    )


class Recipe(models.Model):
    """Модель рецепта."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(max_length=100, verbose_name='Название')
    image = models.ImageField(
        upload_to='recipes/',
        null=True, blank=True,
        verbose_name='Изображение'
    )
    text = models.TextField(blank=True, verbose_name='Описание')
    ingredients = models.ManyToManyField(
        Ingredient,
        through=RecipeIngredient,
        verbose_name='Ингредиенты',
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        verbose_name='Теги'
    )
    cooking_time = models.IntegerField(verbose_name='Время приготовления')
    is_favorited = models.BooleanField(
        default=False,
        verbose_name='В списке избранного'
    )
    is_in_shopping_cart = models.BooleanField(
        default=False,
        verbose_name='В списке покупок'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class FavoriteRecipe(models.Model):
    """Модель связи рецептов и юзеров для формирования списка избранного."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorited'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )


class ShopRecipe(models.Model):
    """Модель связи рецептов и юзеров для формирования списка покупок."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE
    )


class Following(models.Model):
    """Модель подписок и подписчиков."""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
        verbose_name='Автор',
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
