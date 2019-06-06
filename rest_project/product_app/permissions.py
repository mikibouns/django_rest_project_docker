from rest_framework.permissions import BasePermission


class IsAdminOrReadOnly(BasePermission):
    message = 'You must be an administrator'

    def has_permission(self, request, view):
        if request.method in ['GET'] or request.user.is_superuser:
            return True
        return False

