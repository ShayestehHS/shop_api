from django.contrib import admin
from django.utils.html import format_html

from blog.models import Article


@admin.register(Article)
class ArticleModelAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'title', 'user', 'status']
    list_filter = ['status']
    search_fields = ['title', 'slug', 'body']
    readonly_fields = ('id',)
    prepopulated_fields = {'slug': ('name',)}

    def image_tag(self):
        return format_html(f"<img width=100 height=75 style='border-radius: 2px;' src='{self.image.url}'>")

    image_tag.short_description = 'image'
