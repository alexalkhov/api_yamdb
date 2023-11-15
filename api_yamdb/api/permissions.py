from rest_framework import permissions


class IsAuthorModeratorAdminSuperuserOrReadOnly(permissions.BasePermission):
    message = ('Изменение контента доступно '
               'только Автору или Администрации сайта.')

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_admin
                    or request.user.is_moderator
                    or obj.author == request.user
                    )
                )
