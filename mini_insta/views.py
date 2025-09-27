"""Views for the mini_insta app."""


from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Profile
# Create your views here.

class ProfileListView(ListView):
    """Display a list of Profile instances. """
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    """Display a single Profile instance."""

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"