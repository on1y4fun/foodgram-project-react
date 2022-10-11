from rest_framework import exceptions, permissions


class AuthorOrAuthenticated(permissions.BasePermission):
    author_methods = (
        "PATCH",
        "DELETE",
    )

    def has_permission(self, request, view):
        if request.method == "POST" and not request.user.is_authenticated:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_admin:
            return True
        if request.method not in self.author_methods:
            return False
        if not obj.author == request.user:
            return False
        return True


class CreateUserOrAuthenticated(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_admin:
            return True
        return False


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS:
            raise exceptions.MethodNotAllowed(request.method)
        return True


class GetPostOnly(permissions.BasePermission):
    follow_methods = (
        "GET",
        "POST",
    )

    def has_permission(self, request, view):
        return request.method in self.follow_methods
