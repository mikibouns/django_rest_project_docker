from rest_framework.permissions import BasePermission, SAFE_METHODS


class POSTOrNotForUsers(BasePermission):
    '''Метод Post доступен для анонимных пользователей и не доступен для авторизованных, за исключением суперпользователя'''
    message = ''

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in ['GET', 'PUT', 'DELETE'] or request.user.is_superuser:
                return True
            self.message = 'Method \"POST\" not allowed.'
            return False
        else:
            if request.method in ['POST']:
                return True
            return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj == request.user or request.user.is_superuser