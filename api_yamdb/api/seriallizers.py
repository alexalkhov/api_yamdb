from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Comment, Review


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
                message= ('На одно произведение '
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
