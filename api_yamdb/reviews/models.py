from django.db import models


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
        return self.name


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
        return self.name


class Title(models.Model):
    """Произведения, к которым пишут отзывы.
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

