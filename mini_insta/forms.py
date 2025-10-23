"""
mini_insta/forms.py
Forms for the mini_insta app.
Name: Rahil Shah
Email: rshah10@bu.edu
"""

from django import forms
from .models import *

class CreatePostForm(forms.ModelForm):
    """Form for creating a new Post."""

    class Meta:
        """ Associate this form with the Post model and specify fields. """
        model = Post
        fields = ['caption']

class UpdateProfileForm(forms.ModelForm):
    """Form for updating an existing Profile."""

    class Meta:
        """ Associate this form with the Profile model and specify fields. """
        model = Profile
        fields = ['display_name', 'profile_image_url', 'bio_text']

class CreateProfileForm(forms.ModelForm):
    """Form for creating a new Profile."""

    class Meta:
        """ Associate this form with the Profile model and specify fields. """
        model = Profile
        fields = ['username', 'display_name', 'bio_text', 'profile_image_url']