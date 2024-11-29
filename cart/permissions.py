from rest_framework.permissions import BasePermission



class IsCartItemOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return obj.cart.user==request.user
        return False