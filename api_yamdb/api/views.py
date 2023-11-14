from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from django_filters.rest_framework import DjangoFilterBackend

from reviews.models import Title


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (...)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = ...
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        ...


class CategoryViewSet:
    pass


class GenreViewSet:
    pass
