from rest_framework import permissions

from order.models import Order


class IsOrderNotPaid(permissions.BasePermission):
    message = "Paid orders can't be delete."

    def has_object_permission(self, request, view, obj: Order):
        """
            If is_paid => return False
            If not is_paid => return True
        """
        return not obj.is_paid


class IsNotHavePaidOrder(permissions.BasePermission):
    message = "You can't have more than one unpaid order at the same time."

    def has_permission(self, request, view):
        order = Order.objects.filter(user=request.user, is_paid=False)
        return not order.exists()



