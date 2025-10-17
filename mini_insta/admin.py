# admin.py
# Python file for registering models with the Django admin interface.

from django.contrib import admin

# Register your models here.

from .models import Profile, Post, Photo, Follow, Comment, Like
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Photo)
admin.site.register(Follow)
admin.site.register(Comment)
admin.site.register(Like)