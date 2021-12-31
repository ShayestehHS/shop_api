from django.conf import settings
from django.core.cache import cache
from rest_framework.exceptions import NotFound
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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


class ArticleChangeStatus(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        article_pk = kwargs.get('pk')
        user = request.user
        article = Article.objects.filter(author=user, pk=article_pk).only('id','is_published')
        if not article.exists():
            return Response({'Result': "Article not found."}, status=403)
        article = article.first()

        article.is_published = not article.is_published
        article.save(update_fields=['is_published'])
        return Response({'Result': f'Article with ID={article.id} is published.'})


class ArticleCreate(CreateAPIView):
    serializer_class = ArticleCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleRetrieve(RetrieveAPIView):
    serializer_class = ArticleDetailSerializer

    def get_object(self):
        obj = Article.objects \
            .filter(pk=self.kwargs.get('pk')) \
            .select_related('author') \
            .only(*self.serializer_class.Meta.fields, 'id', 'hits', 'slug')

        if not obj.exists(): raise NotFound(detail="Article not found", code=404)
        obj.first()
        obj.hits += 1  # should be in 'only'
        obj.save(update_fields=['hits'])  # save method use 'slug'
        return obj
