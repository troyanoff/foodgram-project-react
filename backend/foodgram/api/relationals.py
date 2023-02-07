from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class FollowRelatedField(serializers.RelatedField):
    """Зависимость поля 'is_subscribed' в сериализаторе пользователя."""

    def to_representation(self, value):
        user = self.context['request'].user
        return value in user.following.all()
