from django.contrib import admin

from order.models import Order, OrderItem


@admin.register(OrderItem)
class OrderItemModelAdmin(admin.ModelAdmin):
    readonly_fields = ['calculated_discount', 'calculated_price', 'id']
    list_per_page = 10
    list_display_links = ['order']
    list_display = ['order', 'product', 'calculated_price', 'calculated_discount']


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'payable_amount', 'timestamp']
    list_display_links = ['user']
    list_display = ['user', 'is_paid', 'payable_amount']
    list_filter = ['is_paid']
