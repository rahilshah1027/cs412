# File: views.py
# Author: Rahil Shah (rshah10@bu.edu),9/12/25
# Description: Python file for all the views of the app

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time, random

quotes_list = [
    "“Two things are infinite: the universe and human stupidity; and I'm not sure about the universe.”",
    "“There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.”",
    "“If you can't explain it to a six year old, you don't understand it yourself.”"
] # List of all hardcoded quotes

images_list = [
    "https://www.nobelprize.org/images/einstein-1921-portrait-photo-3469-landscape-gallery.jpg",
    "https://static.nationalgeographic.es/files/styles/image_3200/public/01_genius_quiz_einstein.webp?w=1600&h=2044&q=100",
    "https://upload.wikimedia.org/wikipedia/commons/1/16/Einstein_1933.jpg"
] # List of all hardcoded images

# Create your views here.
def home(request):
    """ View function for home page """
    template_name = "quotes/quote.html"
    context = {
        "quote": random.choice(quotes_list),
        "image": random.choice(images_list),
    }
    return render(request, template_name, context)

def quote(request):
    """ View function for quote page """
    template_name = "quotes/quote.html"
    context = {
        "quote": random.choice(quotes_list),
        "image": random.choice(images_list),
    }
    return render(request, template_name, context)

def show_all(request):
    """ View function for show_all page """
    template_name = "quotes/show_all.html"
    context = {
        "quotes": quotes_list,
        "images": images_list,
    }
    return render(request, template_name, context)

def about(request):
    """ View function for about page """
    template_name = "quotes/about.html"
    return render(request, template_name)