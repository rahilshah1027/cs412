"""URL patterns for the mini_insta app.

Provides routes to list all profiles and to view a single profile's detail.
"""

from django.urls import path
from .views import ProfileListView, ProfileDetailView, PostDetailView

urlpatterns = [
    path('', ProfileListView.as_view(), name="show_all_profiles"),
    path('profile/<int:pk>', ProfileDetailView.as_view(), name='show_profile'),
    path('post/<int:pk>', PostDetailView.as_view(), name='show_post'),
]