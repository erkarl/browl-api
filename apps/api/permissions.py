from rest_framework import permissions

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class IsAccountAdminOrReadOnly(permissions.BasePermission):
    """
    The request is authenticated as an admin, or is a read-only request.
    """

    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS or
           request.user and
           request.user.is_staff):
            return True
        return False
