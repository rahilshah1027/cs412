# voter_analytics/urls.py
# Name: Rahil Shah
# Email: rshah10@bu.edu
# File contains URL patterns for voter_analytics app


from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path(r'', views.VoterListView.as_view(), name='voters'),
    path(r'voter/<int:pk>/', views.VoterDetailView.as_view(), name='voter'),
    path(r'graphs/', views.GraphsView.as_view(), name='graphs'),
]
