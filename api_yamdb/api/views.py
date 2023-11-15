from api_yamdb.settings import SENT_CODE_EMAIL
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from reviews.models import User
from .serializers import (
    TokenCreateSerializer,
    UserCreateSerializer,
    UserSerializer,
    CategorySerializer,
    GenreSerializer,
)
from .mixins import MixinCategoryAndGenre

from reviews.models import Category, Genre, Title


class UserCreateViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания пользователя и отправки кода подтверждения."""

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
    """Вьюсет для получения токена пользователя."""

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
    """Вьюсет для работы с профилем полязователя."""

    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser)
    queryset = User.objects.all()
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        detail=False,
        methods=['get', 'patch', 'delete'],
        url_path=r'(?P<username>[\w.@+-]+)'
    )
    def get_action_with_username(self, request, username):
        """Управление профилем пользователя по его username."""
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
