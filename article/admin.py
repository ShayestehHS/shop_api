from django.contrib import admin
from django.utils.html import format_html

from article.models import Article


@admin.register(Article)
class ArticleModelAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'title', 'author', 'is_published']
    list_filter = ['is_published']
    search_fields = ['title', 'slug', 'body']
    readonly_fields = ('id',)
    prepopulated_fields = {'slug': ('title',)}

    def image_tag(self, obj):
        return format_html(f"<img width=50 height=50 style='border-radius: 2px;' src='{obj.image.url}'>")

    image_tag.short_description = 'image'
