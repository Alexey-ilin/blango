from rest_framework import permissions
from ..models import Post

class AuthorModifyPostOrReadOnly(permissions.IsAuthenticatedOrReadOnly):

    def has_object_permission(self, request, view, obj: Post):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class IsAdminUserForObject(permissions.IsAdminUser):

    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_staff)

        
        
        