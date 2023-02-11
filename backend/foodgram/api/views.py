from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

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
    # permission_classes = (IsAuthenticated, )


class UserViewSet(viewsets.ModelViewSet):
    """Обработка операций с пользователями."""

    queryset = serializers.User.objects.all()
    serializer_class = serializers.UserSerializer


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
