from rest_framework import permissions
from users.models import User

from reviews.models import User


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated
                and request.user.role == 'admin')
        )


class IsAuthorModeratorAdminSuperuserOrReadOnly(permissions.BasePermission):
    message = ('Изменение контента доступно '
               'только Автору или Администрации сайта.')

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.author == request.user:
            return True
        if request.user.role == 'admin':
            return True
        if request.user.role == 'moderator':
            return True
        return False


class UserPermission(permissions.BasePermission):
    message = ('Ограничение действий для эндпоиста username.')

    def has_permission(self, request, view):
        if request.method in [
            'DELETE', 'PATCH', 'GET'
        ]:
            return (
                request.user.is_authenticated
                and (request.user.role == User.Role.admin
                     or request.user.is_superuser)
            )
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )
