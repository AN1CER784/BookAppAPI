from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrAuthenticatedReadOnly(BasePermission):
    """
    Кастомный Permission,
    дает доступ админу на выполнение всех методов
    и аутентифицированным пользователям выполнение безопасных методов.
    """
    def has_permission(self, request, view):
        if bool(request.user and request.user.is_authenticated) and (request.method in SAFE_METHODS):
            return True
        return bool(request.user and request.user.is_staff)
