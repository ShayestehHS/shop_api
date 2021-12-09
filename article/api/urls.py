from django.urls import path

from article.api import views

app_name = 'article'

urlpatterns = [
    path('list/', views.ArticleList.as_view(), name="list"),
    path('create/', views.ArticleCreate.as_view(), name="create"),
    path('detail/<int:pk>/', views.ArticleDetail.as_view(), name="detail"),
]
