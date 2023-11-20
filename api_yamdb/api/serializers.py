from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Comment, Genre, Review, User


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели пользователя"""
    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'bio', 'role'
        )


class UserCreateSerializer(serializers.Serializer):
    """Сериалайзер для создания новых пользователей"""

    email = serializers.EmailField(required=True, max_length=254)
    username = serializers.CharField(
        required=True,
        validators=[RegexValidator(regex=r'^[\w.@+-]+\Z')],
        max_length=150
    )

    class Meta:
        model = User
        fields = ('email', 'username')

    def validate(self, data):
        email = data['email']
        username = data['username']

        user_with_email = User.objects.filter(email=email)
        user_with_username = User.objects.filter(username=username)

        if user_with_email.exists() and not user_with_username.exists():
            raise serializers.ValidationError(
                'Пользователь с таким email уже существует.'
            )

        if (user_with_username.exists()
                and user_with_username.first().email != email):
            raise serializers.ValidationError(
                'Несоответствующий email для существующего пользователя.'
            )

        if data['username'] == 'me':
            raise serializers.ValidationError(
                'Нельзя использовать это имя пользователя'
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
