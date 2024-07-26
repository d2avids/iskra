from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet


class ListRetrieveViewSet(mixins.RetrieveModelMixin,
                          mixins.ListModelMixin,
                          GenericViewSet):
    """Миксин, разрешающий только методы чтения."""
    pass


class ListRetrieveCreateDeleteViewSet(mixins.ListModelMixin,
                                      mixins.RetrieveModelMixin,
                                      mixins.CreateModelMixin,
                                      mixins.DestroyModelMixin,
                                      GenericViewSet):
    """Миксин, разрешающий методы чтения, создания и удаления."""
    pass


class ListRetrieveCreateViewSet(mixins.ListModelMixin,
                                      mixins.RetrieveModelMixin,
                                      mixins.CreateModelMixin,
                                      GenericViewSet):
    """Миксин, разрешающий методы чтения и создания."""
    pass
