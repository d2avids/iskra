from rest_framework.pagination import LimitOffsetPagination


class Limit250OffsetPagination(LimitOffsetPagination):
    default_limit = 100
    max_limit = 250
