from django.urls import include, path
from rest_framework import routers

from .views import TokenCreateViewSet, UserCreateViewSet, UserViewSet, CategoryViewSet, GenreViewSet, TitleViewSet

v1_router = routers.SimpleRouter()
v1_router.register('users', UserViewSet, basename='users')
v1_router.register('titles', TitleViewSet, basename='titles')
v1_router.register('categories', CategoryViewSet, basename='сategories')
v1_router.register('genres', GenreViewSet, basename='genres')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    path(
        'v1/auth/singup/',
        UserCreateViewSet.as_view({'post': 'create'}),
        name='singup'
    ),
    path(
        'v1/auth/token',
        TokenCreateViewSet.as_view({'post': 'create'}),
        name='token'
    )
]
