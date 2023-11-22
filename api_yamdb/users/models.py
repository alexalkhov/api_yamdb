from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    """Модель пользователя."""

    class Role(models.TextChoices):
        user = 'user'
        moderator = 'moderator'
        admin = 'admin'
    username = models.CharField(
        'логин',
        max_length=150,
        unique=True,
        validators=[RegexValidator(regex=r'^[\w.@+-]+\Z')]
    )
    first_name = models.TextField('имя', max_length=150, blank=True)
    last_name = models.TextField('фамилия', max_length=150, blank=True)
    email = models.EmailField(max_length=254, unique=True)
    bio = models.TextField('биография', blank=True)
    role = models.CharField(
        'роль',
        max_length=150,
        choices=Role.choices,
        default=Role.user
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
