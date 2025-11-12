"""
dadjokes/serializers.py
Serializers for the dadjokes app.
Name: Rahil Shah
Email: rshah10@bu.edu
"""

from rest_framework import serializers
from .models import Joke, Picture

class JokeSerializer(serializers.ModelSerializer):
    """ Serializer for the Joke model. """
    class Meta:
        model = Joke
        fields = ['id', 'text', 'name', 'timestamp']

    def create(self, validated_data):
        joke = Joke.objects.create(**validated_data)
        joke.save()
        return joke
    

class PictureSerializer(serializers.ModelSerializer):
    """ Serializer for the Picture model. """
    class Meta:
        model = Picture
        fields = ['id', 'image_url', 'name', 'timestamp']

    def create(self, validated_data):
        picture = Picture.objects.create(**validated_data)
        picture.save()
        return picture