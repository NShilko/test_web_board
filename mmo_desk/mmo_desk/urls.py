"""mmo_desk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from sign.views import ConfirmEmailView
from ckeditor_uploader import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('publ/', include('publication.urls')),
    path('pages/', include('django.contrib.flatpages.urls')),
    #path('', include('protect.urls')),
    path('sign/', include('sign.urls')),
    #path('', name='home'),
    path('activate/<int:user_id>', ConfirmEmailView, name='confirm_email'),
    re_path(r'^ckeditor/', include('ckeditor_uploader.urls')),
    re_path(r'^upload/', views.upload, name='ckeditor_upload'),
    re_path(r'^browse/', views.browse, name='ckeditor_browse'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

