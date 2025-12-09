# project/models.py
# Rahil Shah, rshah10@bu.edu
# Models for the "project" app

from django.db import models

# Create your models here.

class Game(models.Model):
    """
    A Game model

    Attributes:
    title: The title of the game
    description: A brief description of the game
    release_date: The release date of the game
    genre: The genre of the game
    image: An image representing the game
    """
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    release_date = models.DateField()
    genre = models.ForeignKey('Genre', on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='game_images/', blank=True, null=True)

    def __str__(self):
        return self.title

class Genre(models.Model):
    """
    A Genre model

    Attributes:
    name: The name of the genre
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Platform(models.Model):
    """
    A Platform model

    Attributes:
    name: The name of the platform
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Review(models.Model):
    """
    A Review model

    Attributes:
    game: The game being reviewed
    reviewer_name: Name of the reviewer
    rating: Rating given to the game (out of 10)
    body: The body of the review
    created_at: The date the review was created
    platform: The platform the game was reviewed on
    """

    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='reviews')
    reviewer_name = models.CharField(max_length=100)
    rating = models.IntegerField()
    body = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    platform = models.ForeignKey(Platform, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Review of {self.game.title} by {self.reviewer_name}'
