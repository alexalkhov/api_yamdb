from django.core.validators import RegexValidator
from django.db import models


class User(models.Model):
    """Модель пользователя."""
    class Role(models.TextChoices):
        user = 'user'
        moderator = 'moderator'
        admin = 'admin'
    username = models.TextField(
        'логин',
        max_length=150,
        unique=True,
        validators=[RegexValidator(regex=r'^[\w.@+-]+\Z')])
    first_name = models.TextField('имя', max_length=150, blank=True)
    last_name = models.TextField('фамилия', max_length=150, blank=True)
    email = models.EmailField(unique=True, max_length=254)
    bio = models.TextField('биография', blank=True)
    role = models.CharField('роль',
                            max_length=150,
                            choices=Role.choices,
                            default=Role.user)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
