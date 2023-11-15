from api_yamdb.settings import SENT_CODE_EMAIL
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from api.mixins import MixinCategoryAndGenre
from api.permissions import IsAuthorModeratorAdminSuperuserOrReadOnly
from api.serializers import (CategorySerializer, CommentSeriallizers,
                             GenreSerializer, ReviewSeriallizers,
                             TokenCreateSerializer, UserCreateSerializer,
                             UserSerializer)
from reviews.models import Category, Genre, Review, Title, User


class UserCreateViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания пользователя и отправки кода подтверждения"""
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        user = User(**serializer.validated_data)
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код для входа',
            message=f'Ваш код для входа на портал YAMDB: {confirmation_code}',
            authors_email=SENT_CODE_EMAIL,
            users_email=[email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenCreateViewSet(viewsets.ModelViewSet):
    """Вьюсет для получения токена пользователя"""
    serializer_class = TokenCreateSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        user = authenticate(
            request,
            username=username,
            confirmation_code=confirmation_code
        )
        if user is None:
            return Response(
                'Пользователь не найден',
                status=status.HTTP_404_NOT_FOUND
            )
        login(request, user)
        token = default_token_generator.make_token(user)
        return Response({'token': token}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с профилем полязователя"""
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch', 'delete'],
        url_path=r'(?P<username>[\w.@+-]+)'
    )
    def get_action_with_username(self, request, username):
        """Управление профилем пользователя по его username"""
        pass


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


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с отзывами"""
    serializer_class = ReviewSeriallizers
    permission_classes = (
        IsAuthorModeratorAdminSuperuserOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly,
    )
    pagination_class = LimitOffsetPagination

    def get_title(self):
        return get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с комментариями"""
    serializer_class = CommentSeriallizers
    permission_classes = (
        IsAuthorModeratorAdminSuperuserOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly,
    )
    pagination_class = LimitOffsetPagination

    def get_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
