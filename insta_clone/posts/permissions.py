from rest_framework import permissions
from rest_framework.request import Request
from rest_framework.views import View
from typing import Any


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to allow only the owner of a post to modify or delete it.
    Read-only access is granted to all users.
    """

    def has_object_permission(self, request: Request, view: View, obj: Any) -> bool:
        """
        Check if the request has permission to access the object.

        - Read permissions (GET, HEAD, OPTIONS) are allowed for everyone.
        - Write permissions (PUT, PATCH, DELETE) are allowed only for the post owner.
        """
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
