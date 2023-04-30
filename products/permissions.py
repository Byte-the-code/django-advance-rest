from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSeller(BasePermission):
    """
    Allows access only to seller users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.user_type == 'seller'

class IsSellerOrReadOnly(BasePermission):
    """
    Allows access to all users, but only sellers can edit.
    """

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user.is_authenticated and
            request.user.user_type == 'seller'
        )