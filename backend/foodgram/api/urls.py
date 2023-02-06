from django.urls import include, path
from rest_framework import routers

from api import views

app_name = 'api'

router = routers.DefaultRouter()

router.register('ingredients', views.IngredientViewSet, basename='ingredients')

urlpatterns = [
    path('', include(router.urls)),
]
