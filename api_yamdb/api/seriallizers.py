from django.forms import ValidationError
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
        read_only_fields = ('author', 'title',)

    def validate(self, data):
        if Review.objects.filter(
            author=self.context['request'].user,
            title_id=self.context['title_id'].kwargs.get('title_id')
        ).exists() and self.context['request'].method == 'POST':
            raise ValidationError(
                'На одно произведение пользователь '
                'может оставить только один отзыв.'
            )
        return data


class CommentSeriallizers(serializers.ModelSerializer):
    """Сериализатор комментариев"""
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('author', 'review')
