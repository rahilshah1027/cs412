# project/views.py
# Rahil Shah, rshah10@bu.edu
# Views for the "project" app

from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Game, Genre, Platform, Review
from .forms import CreateGameForm, CreateReviewForm


# Create your views here.
def home(request):
    """
    View for the welcome page
    """
    return render(request, 'project/welcome.html')

class GameListView(ListView):
    """
    View for GameList
    """
    model = Game
    template_name = 'project/game_list.html'
    context_object_name = 'games'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['years'] = range(1950, 2026)
        context['genres'] = Genre.objects.all()
        return context

    def get_queryset(self):
        """
        Override the default queryset to order voters by voter_score descending.
        """
        results = super().get_queryset()
        if 'genre' in self.request.GET:
            genre = self.request.GET.get('genre')
            if genre:
                results = results.filter(genre__name__istartswith=genre)
        if 'year' in self.request.GET:
            year = self.request.GET.get("year")
            if year:
                results = results.filter(release_date__year=year)
        return results.order_by('title')

class GameDetailView(DetailView):
    """
    View for Game Detail
    """
    model = Game
    template_name = 'project/game_detail.html'
    context_object_name = 'game'

class ReviewListView(ListView):
    """
    View for ReviewList
    """

    model = Review
    template_name = "project/review_list.html"
    context_object_name = "reviews"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['values'] = range(0, 10)
        context['genres'] = Genre.objects.all()
        context['platforms'] = Platform.objects.all()
        context['years'] = range(1950, 2026)
        return context

    def get_queryset(self):
        """
        Override the default queryset to order voters by voter_score descending.
        """
        results = super().get_queryset()
        if 'genre' in self.request.GET:
            genre = self.request.GET.get('genre')
            if genre:
                results = results.filter(game__genre__name=genre)
        if 'year' in self.request.GET:
            year = self.request.GET.get("year")
            if year:
                results = results.filter(game__release_date__year=year)
        if 'platform' in self.request.GET:
            platform = self.request.GET.get("platform")
            if platform:
                results = results.filter(platform__id=platform)
        if 'min_rating' in self.request.GET:
            min_rating = self.request.GET.get("min_rating")
            if min_rating:
                results = results.filter(rating__gte=min_rating)
        if 'max_rating' in self.request.GET:
            max_rating = self.request.GET.get("max_rating")
            if max_rating:
                results = results.filter(rating__lte=max_rating)
        return results.order_by('created_at')

class ReviewDetailView(DetailView):
    """
    View for Review Detail
    """
    model = Review
    template_name = "project/review_detail.html"
    context_object_name = "review"

class AddGameView(CreateView):
    """
    View for adding a new Game
    """
    model = Game
    template_name = "project/add_game_form.html"
    form_class = CreateGameForm
    success_url = reverse_lazy('game_list')

class AddReviewView(CreateView):
    """
    View for adding a new Review
    """
    model = Review
    template_name = "project/add_review_form.html"
    form_class = CreateReviewForm
    success_url = reverse_lazy('review_list')

    def form_valid(self, form):

        return super().form_valid(form)

class UpdateReviewView(UpdateView):
    """
    View for editing an existing Review
    """
    model = Review
    form_class = CreateReviewForm
    template_name = "project/update_review_form.html"
    success_url = reverse_lazy("review_list")

class DeleteReviewView(DeleteView):
    """
    View for deleting an existing Review
    """
    model = Review
    template_name = "project/delete_review_confirm.html"
    success_url = reverse_lazy("review_list")