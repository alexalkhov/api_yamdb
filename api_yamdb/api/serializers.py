from django.core.validators import RegexValidator
from django.db.models import Avg
from django.forms import ValidationError
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from django.utils import timezone
from reviews.models import Category, Comment, Genre, Title, Review, User


class UserSerializer(serializers.ModelSerializer):
    """Сериалайзер для модели пользователя."""

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
    """Сериалайзер для создания Токена."""

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


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания объекта Title."""

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )

    def validate_year(self, value):
        current_year = timezone.now().year
        if value and int(value) > current_year:
            raise serializers.ValidationError(
                'Нельзя добавлять произведения, которые еще не вышли.'
            )
        return value

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year',
            'description', 'genre',
            'category',
        )


class TitleReadSerializer(serializers.ModelSerializer):
    """Сериализатор для прочтения объекта Title."""

    genre = GenreSerializer(
        many=True,
        read_only=True,
    )
    category = CategorySerializer(
        read_only=True,
    )
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'year',
            'rating', 'description',
            'genre', 'category',
        )

    def get_rating(self, obj):
        if obj.reviews.count() == 0:
            return None
        return (Review.objects
                .filter(title=obj)
                .aggregate(rating=Avg('score'))['rating']
                )


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов"""

    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Review
        read_only_fields = ('author', 'title',)

    def validate(self, data):
        if Review.objects.filter(
            author=self.context['request'].user,
            title_id=self.context['view'].kwargs.get('title_id')
        ).exists() and self.context['request'].method == 'POST':
            raise ValidationError(
                'На одно произведение пользователь '
                'может оставить только один отзыв.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев"""

    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('author', 'review')
