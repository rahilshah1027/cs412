# File: urls.py
# Author: Rahil Shah (rshah10@bu.edu), 9/14/25
# Description: Python file for all the urls of the app

from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', views.home, name='home'),
    path(r'main/', views.main, name='main'),
    path(r'order/', views.order, name='order'),
    path(r'confirmation/', views.confirmation, name='confirmation'),
]