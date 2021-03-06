"""shop_api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('article/', include('article.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.decorators.cache import cache_page

from shop_api.views import HomeAPIView

urlpatterns = [
    path('', cache_page(60 * 15)(HomeAPIView.as_view()), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.api.urls')),
    path('article/', include('article.api.urls', namespace='article')),
    path('product/', include('product.api.urls', namespace='product')),
    path('order/', include('order.api.urls', namespace='order')),
    path('cart/', include('cart.api.urls', namespace='cart')),

    # Third party apps
    path('comments/', include('django_comments_xtd.urls')),
]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls import url
    from django.conf.urls.static import static

    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
