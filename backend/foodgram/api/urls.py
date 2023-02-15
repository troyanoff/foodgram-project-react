from django.urls import include, path
from rest_framework import routers

from api import views

app_name = 'api'

router = routers.DefaultRouter()

router.register('ingredients', views.IngredientViewSet, basename='ingredients')
router.register('tags', views.TagViewSet, basename='tags')
router.register('recipes', views.RecipeViewSet, basename='recipes')
router.register('users', views.UserViewSet, basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/login/', views.get_token, name='get_token'),
    path('auth/token/logout/', views.logout_token, name='logout_token'),
    path(
        'recipes/<int:recipe_id>/shopping_cart/',
        views.shopping_cart,
        name='shopping_cart'
    ),
    path(
        'recipes/<int:recipe_id>/favorite/',
        views.farorited,
        name='favorited'
    ),
    path(
        'users/<int:author_id>/subscribe/',
        views.subscribe,
        name='subscribe'
    ),
]
