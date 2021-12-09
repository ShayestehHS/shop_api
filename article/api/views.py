from django.conf import settings
from django.core.cache import cache
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated

from article.api.serializers import ArticleCreateSerializer, ArticleDetailSerializer, ArticleListSerializer
from article.models import Article


class ArticlePagination(PageNumberPagination):
    page_size = settings.ARTICLE_PAGINATION
    page_size_query_param = 'page_size'
    max_page_size = settings.ARTICLE_MAX_PAGINATION


class ArticleList(ListAPIView):
    serializer_class = ArticleListSerializer
    pagination_class = ArticlePagination
    search_fields = ['name', 'slug', 'body']

    def get_queryset(self):
        if 'articles' in cache:
            articles = cache.get('articles')
            return articles

        queryset = Article.objects.filter(is_published=True)
        if queryset.count() > 0: cache.set('articles', queryset)
        return queryset


class ArticleCreate(CreateAPIView):
    serializer_class = ArticleCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleDetail(RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = ArticleDetailSerializer

    def get_object(self):
        obj = Article.objects \
            .filter(pk=self.kwargs.get('pk')) \
            .select_related('author') \
            .only(*self.serializer_class.Meta.fields, 'id', 'hits', 'slug') \
            .first()
        obj.hits += 1  # need hits
        obj.save(update_fields=['hits'])  # need slug
        return obj
