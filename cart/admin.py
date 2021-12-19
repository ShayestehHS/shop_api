from django.contrib import admin

from cart.models import Cart


@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
