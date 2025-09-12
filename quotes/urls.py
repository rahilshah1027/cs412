# File: urls.py
# Author: Rahil Shah (rshah10@bu.edu),9/12/25
# Description: Python file for all the urls of the app

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', views.home, name='home'),
    path(r'quote/', views.quote, name='quote'),
    path(r'show_all/', views.show_all, name='show_all'),
    path(r'about/', views.about, name='about'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)