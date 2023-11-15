from django.urls import path
from rest_framework import routers

from .views import TokenCreateViewSet, UserCreateViewSet, UserViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
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
