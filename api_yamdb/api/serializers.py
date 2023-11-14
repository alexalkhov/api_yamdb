from rest_framework import serializers
from .models import User


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


class CreateUserTokenSerializer(serializers.ModelSerializer):
    """Сериалайзер для создания Токена"""
    username = serializers.CharField(
        required=True,
        max_lenght=150,
        regex=r'^[\w.@+-]+\Z'
    )
    confirmation_code = serializers.CharField(required=True, max_lenght=150)

    class Meta:
        model = User
        field = ('username', 'confirmation_code')
