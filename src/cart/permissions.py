from rest_framework import permissions


class IsCartHaveProduct(permissions.BasePermission):
    message = "You don't have any product in your cart."

    def has_object_permission(self, request, view, obj):
        if obj.products.count == 0:
            return False
        return True
