from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Comment, Genre, Review, User


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели пользователя"""
    class Meta:
        model = User
        fields = '__all__'


class UserCreateSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания новых пользователей"""
    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать это имя пользователя'
            )
        if User.objects.filter(username=data['username']):
            raise serializers.ValidationError(
                'Такое имя пользователя уже существует'
            )
        if User.objects.filter(email=data['email']):
            raise serializers.ValidationError(
                'Такой адрес электронной почты уже существует'
            )
        return data


class TokenCreateSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания Токена"""
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[RegexValidator(regex=r'^[\w.@+-]+\Z')]
    )
    confirmation_code = serializers.CharField(required=True, max_length=150)

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        model = Category
        fields = ('name', 'slug',)


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        model = Genre
        fields = ('name', 'slug',)


class TitleSerializer:
    pass


class ReviewSeriallizers(serializers.ModelSerializer):
    """Сериализатор отзывов"""
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only = ('author', 'title',)
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Review.objects.all(),
                fields=['user', 'reviews'],
                message=('На одно произведение '
                         'пользователь может оставить только один отзыв.')
            )
        ]


class CommentSeriallizers(serializers.ModelSerializer):
    """Сериализатор комментариев"""
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only = ('author', 'review')
