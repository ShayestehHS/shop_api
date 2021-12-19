from django.contrib import admin

from order.models import Order


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    readonly_fields = ['id', 'payable_amount', 'timestamp']
    list_display_links = ['user']
    list_display = ['user', 'is_paid', 'payable_amount']
    list_filter = ['is_paid']
