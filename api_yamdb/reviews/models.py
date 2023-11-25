from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User


class Category(models.Model):
    """Категории (типы) произведений."""

    name = models.CharField(
        'Категории',
        max_length=256,
    )
    slug = models.SlugField(
        'URL категории',
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name} {self.slug}'


class Genre(models.Model):
    """Категории жанров."""

    name = models.CharField(
        'Жанры',
        max_length=256,
    )
    slug = models.SlugField(
        'URL жанра',
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'{self.name} {self.slug}'


class Title(models.Model):
    """
    Произведения, к которым пишут отзывы.
    (определённый фильм, книга или песенка).
    """

    name = models.CharField(
        'Название',
        max_length=256,
    )
    year = models.IntegerField(
        'Год выпуска',
    )
    description = models.TextField(
        'Описание',
        blank=True,
        null=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Slug жанра',
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Slug категории',
    )

    class Meta:
        ordering = ('-year',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзывов."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение для оценки'
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )
    text = models.TextField('Текст отзыва')
    score = models.PositiveSmallIntegerField(
        'Оценка произведения',
        validators=[
            MinValueValidator(1, message='Оценка от 1'),
            MaxValueValidator(10, message='Оценка до 10'),
        ]
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'), name='unique_review'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментариев."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text
