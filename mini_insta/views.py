"""
mini_insta/views.py
Name: Rahil Shah
Email: rshah10@bu.edu
Includes all the views for the mini_insta app.
"""

from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Profile, Post, Photo
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
# Create your views here.

class MyLoginRequiredMixin(LoginRequiredMixin):
    """Mixin to ensure the user is logged in to access the view."""
    
    def get_logged_in_profile(self):
        """Return the Profile instance for the logged-in user."""
        return Profile.objects.get(user=self.request.user)

    def get_login_url(self):
        """Redirect to login if not authenticated."""
        return reverse('login')

    def get_context_data(self, **kwargs):
        """Add the logged-in user's profile to the template context."""
        context = super().get_context_data(**kwargs)
        context['profile'] = self.get_logged_in_profile()
        return context

class ProfileListView(ListView):
    """Display a list of Profile instances. """
    model = Profile
    template_name = "mini_insta/show_all_profiles.html"
    context_object_name = "profiles"

class ProfileDetailView(DetailView):
    """Display a single Profile instance."""

    model = Profile
    template_name = "mini_insta/show_profile.html"
    context_object_name = "profile"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['logged_in_profile'] = Profile.objects.get(user=self.request.user)
        return context

class PostDetailView(DetailView):
    """Display a single Post instance."""

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['logged_in_profile'] = Profile.objects.get(user=self.request.user)
        return context

class CreatePostView(MyLoginRequiredMixin, CreateView):
    """View for creating a new Post."""

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"
    
    def get_login_url(self):
        return reverse('login')

    def get_context_data(self, **kwargs):
        """Add the profile to the context."""
        context = super().get_context_data(**kwargs)
        profile = self.get_logged_in_profile()
        context['profile'] = profile
        return context

    def form_valid(self, form):
        """Associate the new post with the correct profile."""
        form.instance.profile = self.get_logged_in_profile()
        response = super().form_valid(form)
        files = self.request.FILES.getlist('image_files')
        for file in files:
            Photo.objects.create(post=form.instance, image_file=file)
        return response

    def get_object(self):
        """Return the Profile instance for the logged-in user."""
        return self.get_logged_in_profile()

    def get_success_url(self):
        """Redirect back to the profile page after creating a post."""
        return reverse('show_profile', kwargs={'pk': self.get_object().pk})

class UpdateProfileView(MyLoginRequiredMixin, UpdateView):
    """View for updating an existing Profile."""

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"
    context_object_name = "profile"

    def get_object(self):
        """Return the Profile instance for the logged-in user."""
        return self.get_logged_in_profile()

    def get_success_url(self):
        """Redirect back to the profile page after updating."""
        return reverse('show_profile', kwargs={'pk': self.get_object().pk})
    
class DeletePostView(DeleteView):
    """View for deleting an existing Post."""

    model = Post
    template_name = "mini_insta/delete_post_form.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        """Provide context data for the delete confirmation template."""
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['post'] = post
        context['profile'] = post.profile
        return context

    def get_success_url(self):
        """Redirect back to the profile page after deleting a post."""
        pk = self.object.profile.pk
        return reverse('show_profile', kwargs={'pk': pk})
    
class UpdatePostView(UpdateView):
    """View for updating an existing Post."""

    model = Post
    fields = ['caption']
    template_name = "mini_insta/update_post_form.html"
    context_object_name = "post"

    def get_context_data(self, **kwargs):
        """Provide context data for the update confirmation template."""
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['post'] = post
        return context

    def get_success_url(self):
        """Redirect back to the post page after updating."""
        pk = self.kwargs['pk']
        return reverse('show_post', kwargs={'pk': pk})
    
class ShowFollowersView(DetailView):
    """Display all followers of a given profile."""

    model = Profile
    template_name = "mini_insta/show_followers.html"
    context_object_name = "profile"

class ShowFollowingView(DetailView):
    """Display all profiles that a given profile is following."""

    model = Profile
    template_name = "mini_insta/show_following.html"
    context_object_name = "profile"

class PostFeedListView(MyLoginRequiredMixin, ListView):
    """Display a feed of posts from profiles that the user follows."""

    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_object(self):
        """Return the Profile instance for the logged-in user."""
        return self.get_logged_in_profile()
    
    def get_queryset(self):
        """Return posts from profiles that the user follows."""
        profile = self.get_logged_in_profile()
        return profile.get_post_feed()

class SearchView(MyLoginRequiredMixin, ListView):
    """View for searching profiles by username or display name."""

    model = Profile
    template_name = "mini_insta/search_results.html"
    context_object_name = "profiles"

    def dispatch(self, request, *args, **kwargs):
        if 'query' not in self.request.GET:
            profile = self.get_logged_in_profile()
            return render(request, 'mini_insta/search.html', {'profile': profile})
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        query = self.request.GET.get('query', '')
        return Post.objects.filter(caption__icontains=query).order_by('-timestamp')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        profile = self.get_logged_in_profile()
        query = self.request.GET.get('query', '')

        if query != '':
            post_results = self.get_queryset()
            profile_results = Profile.objects.filter(username__icontains=query) | Profile.objects.filter(display_name__icontains=query) | Profile.objects.filter(bio_text__icontains=query)

        context['profile'] = profile
        context['query'] = query
        context['post_results'] = post_results
        context['profile_results'] = profile_results
        return context

class CreateProfileView(CreateView):
    """View for creating a new Profile."""

    form_class = CreateProfileForm
    template_name = "mini_insta/create_profile_form.html"

    def get_context_data(self, **kwargs):
        """Add context data for the create profile template."""
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context

    def form_valid(self, form):
        """Create a new User and associate it with the new Profile."""
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()
            login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
            form.instance.user = user
            return super().form_valid(form)
        else:
            print("User form invalid", user_form.errors)
            return self.form_invalid(form)

    def get_success_url(self):
        """Redirect to the newly created profile page after creation."""
        return reverse('show_profile', kwargs={'pk': self.object.pk})
    
class FollowProfileView(MyLoginRequiredMixin, TemplateView):
    """View for following a profile."""

    def dispatch(self, request, *args, **kwargs):
        follower = self.get_logged_in_profile()
        pk = kwargs['pk']
        following = Profile.objects.get(pk=pk)
        if follower != following:
            Follow.objects.create(profile=following, follower_profile=follower)
        return redirect('show_profile', pk=following.pk)
  
class UnfollowProfileView(MyLoginRequiredMixin, TemplateView):
    """View for unfollowing a profile."""

    def dispatch(self, request, *args, **kwargs):
        follower = self.get_logged_in_profile()
        pk = kwargs['pk']
        following = Profile.objects.get(pk=pk)
        follow = Follow.objects.filter(profile=following, follower_profile=follower)
        follow.delete()
        return redirect('show_profile', pk=following.pk)
    
class LikePostView(MyLoginRequiredMixin, TemplateView):
    """View for liking a post."""

    def dispatch(self, request, *args, **kwargs):
        profile = self.get_logged_in_profile()
        pk = kwargs['pk']
        post = Post.objects.get(pk=pk)
        if post.profile != profile:
            Like.objects.create(post=post, profile=profile)
        return redirect('show_post', pk=post.pk)
    
class UnlikePostView(MyLoginRequiredMixin, TemplateView):  
    """View for unliking a post."""

    def dispatch(self, request, *args, **kwargs):
        profile = self.get_logged_in_profile()
        pk = kwargs['pk']
        post = Post.objects.get(pk=pk)
        like = Like.objects.filter(post=post, profile=profile)
        like.delete()
        return redirect('show_post', pk=post.pk)