from rest_framework import serializers

from article.models import Article


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        exclude = ['is_published', 'hits', 'update_time', 'body', 'average_rating']


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'image', 'body']
