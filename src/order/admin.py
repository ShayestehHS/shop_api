from django.contrib import admin

from order.models import Coupon, Order, Price


@admin.register(Coupon)
class OrderModelAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
    list_display = ['__str__', 'is_valid', 'discount_amount', 'discount_percent']
    list_filter = ['is_valid']


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'payable_amount', 'timestamp']
    list_display_links = ['user']
    list_display = ['user', 'is_paid', 'payable_amount']
    list_filter = ['is_paid']


@admin.register(Price)
class PriceModelAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
    list_display = ['amount', 'product', 'order']
