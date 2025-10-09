"""Forms for the mini_insta app."""

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