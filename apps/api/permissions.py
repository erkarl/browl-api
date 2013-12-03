from rest_framework import permissions


class IsAccountAdminOrReadOnly(permissions.BasePermission):
    """
    Allow creating, destroying and modifying the posts
    for only admin users
    """

    def has_permission(self, request, view):
        if request.method == 'GET' or \
           request.method == 'HEAD' or \
           request.method == 'OPTIONS':
            return True
        else:
            if request.user and request.user.is_staff:
                return True
            return False
