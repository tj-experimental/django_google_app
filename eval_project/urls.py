"""eval_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import password_reset_confirm

from map_app import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^address$', views.address_view, name='address'),
    url(r'^reset-address$', views.reset_address, name='reset-address'),
    url(r'^fusion-tables$', views.FusionTableHandler.as_view(),
        name='fusion-tables'),
    url(r'^sync-fusion-table$', views.sync_fusion_table,
        name='sync-fusion-table'),
    url(r'^sync-address$', views.sync_address, name='sync-address'),
    url(r'^oauth2callback$', views.oauth_callback, name='oauth2-callback'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', admin.site.urls),
] + static(settings.STATIC_URL,
           document_root=settings.STATIC_ROOT)
