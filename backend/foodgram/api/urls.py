from django.urls import include, path
from rest_framework import routers

from api import views

app_name = 'api'

router = routers.DefaultRouter()

router.register('ingredients', views.IngredientViewSet, basename='ingredients')
router.register('tags', views.TagViewSet, basename='tags')
router.register('recipes', views.RecipeViewSet, basename='recipes')
router.register('users', views.UserViewSet, basename='users')
router.register(
    r'recipes/(?P<id>\d+)/shopping_cart',
    views.ShoppingViewSet,
    basename='shopping'
)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/login/', views.get_token, name='get_token'),
    path('auth/token/logout/', views.logout_token, name='logout_token'),
]
