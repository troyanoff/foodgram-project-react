from rest_framework import viewsets, mixins


class RetrieveListViewSet(mixins.ListModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    """Вьюсет для получения либо списка, либо одного эл-та."""

    pass
