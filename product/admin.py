from django.contrib import admin
from django.utils.html import format_html

from product.models import Product


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'name', 'count', 'status', 'is_gold', 'is_jewelery']
    list_filter = ['is_gold', 'is_jewelery', 'status']
    search_fields = ['body', 'name', 'slug']
    readonly_fields = ['id']
    prepopulated_fields = {'slug': ('name',)}

    def image_tag(self, obj):
        return format_html(f"<img width=50 height=50 style='border-radius: 2px;' src='{obj.image.url}'>")

    image_tag.short_description = 'image'
