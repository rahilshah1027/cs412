# project/urls.py
# Rahil Shah, rshah10@bu.edu
# URL configurations for the "project" app

from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='welcome'),
    path('games/', GameListView.as_view(), name='game_list'),
    path('game/<int:pk>/', GameDetailView.as_view(), name='game_detail'),
    path('reviews/', ReviewListView.as_view(), name='review_list'),
    path('review/<int:pk>/', ReviewDetailView.as_view(), name='review_detail'),
    path('add_game/', AddGameView.as_view(), name='add_game'),
    path('add_review/', AddReviewView.as_view(), name='add_review'),
    path('review/<int:pk>/update', UpdateReviewView.as_view(), name='update_review'),
    path('review/<int:pk>/delete', DeleteReviewView.as_view(), name='delete_review'),
]