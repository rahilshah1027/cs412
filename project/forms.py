"""
project/forms.py
Forms for the project app.
Name: Rahil Shah
Email: rshah10@bu.edu
"""

from django import forms
from .models import Game, Review, Genre, Platform

class CreateGameForm(forms.ModelForm):
    """Form for creating a new Game."""

    class Meta:
        """ Associate this form with the Game model and specify fields. """
        model = Game
        fields = ['title', 'description', 'release_date', 'genre', 'image']

class CreateReviewForm(forms.ModelForm):
    """Form for creating a new Review."""

    class Meta:
        """ Associate this form with the Review model and specify fields. """
        model = Review
        fields = ['game', 'reviewer_name', 'rating', 'body', 'platform']