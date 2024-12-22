"""fillerlist URL Configuration

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
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.conf.urls import handler404, handler500
from django.views.generic.base import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_page, name='home_page'),
    path('search/', views.search_page, name='search_page'),
    path('id/<id>', views.anime_page, name='anime_page'),
    path('about/', views.about_page, name='about_page'),
    path('404/', views.error_page, name='error_page'),
    path('update/', views.update_file, name='update_page'),
    path('analytics/', views.analytics_page, name='analytics_page'),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
]

handler404 = views.error_page
handler500 = views.error_page
