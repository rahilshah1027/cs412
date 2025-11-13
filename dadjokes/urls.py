"""
dadjokes/urls.py
URL patterns for the dadjokes app.
Name: Rahil Shah
Email: rshah10@bu.edu
Provides routes to list all jokes and pictures, and to submit new jokes and pictures.
"""

from django.urls import path
from .views import *

urlpatterns = [
    path('', RandomView.as_view(), name="home"),
    path('random', RandomView.as_view(), name='random_joke'),
    path('jokes', JokeListView.as_view(), name='joke_list'),
    path('pictures', PictureListView.as_view(), name='picture_list'),
    path('joke/<int:pk>', JokeDetailView.as_view(), name='joke'),
    path('picture/<int:pk>', PictureDetailView.as_view(), name='picture'),

    # API ENDPOINTS
    path('api/', RandomJokeAPIView.as_view(), name='api_root'),
    path('api/random', RandomJokeAPIView.as_view(), name='api_random_joke'),
    path('api/random_picture', RandomPicutureAPIView.as_view(), name='api_random_picture'),
    path('api/jokes', JokeListAPIView.as_view(), name='api_jokes'),
    path('api/joke/<int:pk>', JokeDetailAPIView.as_view(), name='api_joke_detail'),
    path('api/pictures', PictureListAPIView.as_view(), name='api_pictures'),
    path('api/picture/<int:pk>', PictureDetailAPIView.as_view(), name='api_picture_detail'),
]