"""
dadjokes/views.py
Name: Rahil Shah
Email: rshah10@bu.edu
Includes all the views for the dadjokes app.
"""

from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from .models import Joke, Picture
import random
from rest_framework import generics
from .serializers import *

# Create your views here.

class RandomView(TemplateView):
    """ Display a random joke. """
    model = Joke
    template_name = "dadjokes/random_joke.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        jokes = Joke.objects.all()
        if jokes:
            context['joke'] = random.choice(jokes)
        pictures = Picture.objects.all()
        if pictures:
            picture = random.choice(pictures)
            url = picture.image_url
            context['image_url'] = url
        return context

class JokeListView(ListView):
    """ Display a list of Jokes. """
    model = Joke
    template_name = "dadjokes/joke_list.html"
    context_object_name = "jokes"

class PictureListView(ListView):
    """ Display a list of pictures. """
    model = Picture
    template_name = "dadjokes/picture_list.html"
    context_object_name = "pictures"

class JokeDetailView(DetailView):
    """ Display a detailed view of a Joke. """
    model = Joke
    template_name = "dadjokes/joke.html"
    context_object_name = "joke"

class PictureDetailView(DetailView):
    """ Display a list of Jokes. """
    model = Picture
    template_name = "dadjokes/picture.html"
    context_object_name = "picture"

# API VIEWS

class RandomJokeAPIView(generics.RetrieveAPIView):
    """
    An API view to return a random joke.
    """
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

    def get_object(self):
        jokes = self.get_queryset()
        random_joke = random.choice(jokes)
        return random_joke

class JokeListAPIView(generics.ListCreateAPIView):
    """
    An API view to return a listing of all jokes, and to create a new joke.
    """
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer
 
class JokeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    An API view to return details of a joke.
    """
    queryset = Joke.objects.all()
    serializer_class = JokeSerializer

class PictureListAPIView(generics.ListAPIView):
    '''
    An API view to return a listing of all pictures.
    '''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

class PictureDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    '''
    An API view to return details of a picture.
    '''
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer

