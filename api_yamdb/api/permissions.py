from rest_framework import permissions
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
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)
        )


class UserCustomPermission(permissions.BasePermission):
    message = ('Ограничение действий для эндпоиста username')

    def has_permission(self, request, view):
        if view.action == 'list' or request.method in [
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
