from api_yamdb.settings import SENT_CODE_EMAIL
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from reviews.models import Category, Genre, Review, Title, User
from api.filtres import TitleFilter
from api.mixins import MixinCategoryAndGenre
from api.permissions import (IsAdminOrReadOnly,
                             IsAuthorModeratorAdminSuperuserOrReadOnly,
                             UserCustomPermission)
from api.serializers import (CategorySerializer, CommentSerializer,
                             GenreSerializer, ReviewSerializer,
                             TitleCreateSerializer, TitleReadSerializer,
                             TokenCreateSerializer, UserCreateSerializer,
                             UserSerializer)


class UserCreateViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания пользователя и отправки кода подтверждения."""

    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        user, created = User.objects.get_or_create(
            email=email, username=username
        )
        confirmation_code = default_token_generator.make_token(user)
        send_mail(
            subject='Код для входа',
            message=f'Ваш код для входа на портал YAMDB: {confirmation_code}',
            from_email=SENT_CODE_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class TokenCreateViewSet(viewsets.ModelViewSet):
    """Вьюсет для получения токена пользователя."""

    serializer_class = TokenCreateSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        confirmation_code = serializer.validated_data['confirmation_code']
        user = get_object_or_404(User, username=username)
        if not default_token_generator.check_token(user, confirmation_code):
            return Response(
                'Неверный код подтверждения',
                status=status.HTTP_400_BAD_REQUEST
            )
        login(request, user)
        token = default_token_generator.make_token(user)
        return Response({'token': token}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с профилем полязователя."""

    serializer_class = UserSerializer
    permission_classes = (UserCustomPermission,)
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch', 'delete'],
        url_path=r'(?P<username>[\w.@+-]+)',
    )
    def username_actions(self, request, username):
        """Действия с пользователем по username."""
        user = get_object_or_404(User, username=username)
        if request.method == 'GET':
            if not request.auth:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'PATCH':
            serializer = UserSerializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['get'],
        url_path='me',
        permission_classes=[permissions.IsAuthenticated],
    )
    def me(self, request):
        """Получение пользовательских данных."""
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @me.mapping.patch
    def change_me_data(self, request):
        """Изменение пользовательских данных."""
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(MixinCategoryAndGenre):
    """Вьюсет для работы с категориями."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination


class GenreViewSet(MixinCategoryAndGenre):
    """Вьюсет для работы с жанрами."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = LimitOffsetPagination


class TitleViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с произведениями."""

    queryset = Title.objects.all()
    serializer_class = TitleCreateSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return super().get_serializer_class()

    def update(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)

        if len(serializer.validated_data.get('name')) > 256:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет для работы с отзывами."""

    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthorModeratorAdminSuperuserOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly,
    )
    pagination_class = LimitOffsetPagination
    http_method_names = ['get', 'post', 'delete', 'patch']

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
    """Вьюсет для работы с комментариями."""

    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthorModeratorAdminSuperuserOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly,
    )
    pagination_class = LimitOffsetPagination
    http_method_names = ['get', 'post', 'delete', 'patch']

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
