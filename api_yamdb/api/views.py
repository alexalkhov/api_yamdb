from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.pagination import LimitOffsetPagination

from api.permissions import IsAuthorModeratorAdminSuperuserOrReadOnly
from api.seriallizers import CommentSeriallizers, ReviewSeriallizers
from reviews.models import Comment, Review

class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet отзывов"""
    serializer_class = ReviewSeriallizers
    permission_classes = (
        IsAuthorModeratorAdminSuperuserOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly,
    )
    pagination_class = LimitOffsetPagination

    def get_title(self):
        return get_object_or_404(
            Title,
            pk=self.kwargs.get('title_id')
        )
    
    def get_queryset(self):
        return self.get_title().reviews.all()
    
    def perform_create(self, serializer):
        return serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet комментариев"""
    serializer_class = CommentSeriallizers
    permission_classes = (
        IsAuthorModeratorAdminSuperuserOrReadOnly,
        permissions.IsAuthenticatedOrReadOnly,
    )
    pagination_class = LimitOffsetPagination

    def get_review(self):
        return get_object_or_404(
            Review,
            pk=self.kwargs.get('review_id'),
            title_id=self.kwargs.get('title_id')
        )
    
    def get_queryset(self):
        return self.get_review().comments.all()
    
    def perform_create(self, serializer):
        return  serializer.save(
            author=self.request.user,
            review=self.get_review()
        )
