from django.urls import include, path
from rest_framework import routers

from api import views

app_name = 'api'

router = routers.DefaultRouter()

router.register('ingredients', views.IngredientViewSet, basename='ingredients')
router.register('tags', views.TagViewSet, basename='tags')
router.register('recipes', views.RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
]
