from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class ListRetrieveViewSet(mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    """Миксин, разрешающий только методы чтения."""
    pass
