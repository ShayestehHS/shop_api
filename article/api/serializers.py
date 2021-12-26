from django.contrib.auth import get_user_model
from rest_framework import serializers

from article.models import Article

User = get_user_model()


class ArticleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        exclude = ['is_published', 'hits', 'last_update', 'average_rating']


class ArticleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['title', 'image', 'body']


class ArticleDetailSerializer(serializers.ModelSerializer):
    def get_author_username(self, obj: Article):
        return obj.author.username

    author = serializers.SerializerMethodField('get_author_username')

    class Meta:
        model = Article
        fields = ['title', 'body', 'author', 'last_update', 'average_rating']
