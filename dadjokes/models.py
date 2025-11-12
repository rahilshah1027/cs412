"""
dadjokes/models.py
Models for the dadjokes app.
Name: Rahil Shah
Email: rshah10@bu.edu
"""

from django.db import models

# Create your models here.

class Joke(models.Model):
    """
    A joke model

    Attributes:
    text: The text of the joke
    name: name of the contributor
    timestamp: time of submission
    """

    text = models.TextField()
    name = models.CharField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Picture(models.Model):
    """
    A picture model

    Attributes:
    image_url: URL of the image
    name: name of the contributor
    timestamp: time of submission
    """

    image_url = models.URLField()
    name = models.CharField()
    timestamp = models.DateTimeField(auto_now_add=True)