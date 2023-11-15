from rest_framework import filters, viewsets


from api.mixins import MixinCategoryAndGenre
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
)
from reviews.models import Category, Genre, Title


class CategoryViewSet(MixinCategoryAndGenre):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter)
    search_fields = ('name',)
    pagination_class = None


class GenreViewSet(MixinCategoryAndGenre):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter)
    search_fields = ('name',)
    pagination_class = None


class TitleViewSet(viewsets.ModelViewSet):
    pass
