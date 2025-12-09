from django.contrib import admin
from .models import Game, Genre, Platform, Review

# Register your models here.
admin.site.register(Game)
admin.site.register(Genre)
admin.site.register(Platform)
admin.site.register(Review)