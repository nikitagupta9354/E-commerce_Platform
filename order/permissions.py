from rest_framework.permissions import BasePermission

class IsSeller(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role == 'Seller'
        return False
    
class IsBuyer(BasePermission):
    def has_object_permission(self, request, view,obj):
        if request.user.is_authenticated:
            return obj.order.user == request.user
        return False
    
class IsProductSeller(BasePermission):
    def has_object_permission(self, request, view,obj):
        if request.user.is_authenticated:
            return obj.product.seller == request.user
        return False
        