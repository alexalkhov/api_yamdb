from rest_framework import permissions
from users.models import User


class IsAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or (request.user.is_authenticated
                and request.user.role == 'admin')
        )


class ReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class IsModerator(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == 'moderator')

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and request.user.role == 'moderator')


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.role == 'admin')

    def has_object_permission(self, request, view, obj):
        return (request.user.is_authenticated
                and request.user.role == 'admin')


class IsAuthor(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


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
