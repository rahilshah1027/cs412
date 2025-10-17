# mini_insta/views.py
# Includes all the views for the mini_insta app.

from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Profile, Post, Photo
from .forms import CreatePostForm, UpdateProfileForm

# Create your views here.

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

class PostDetailView(DetailView):
    """Display a single Post instance."""

    model = Post
    template_name = "mini_insta/show_post.html"
    context_object_name = "post"

class CreatePostView(CreateView):
    """View for creating a new Post."""

    form_class = CreatePostForm
    template_name = "mini_insta/create_post_form.html"

    def get_context_data(self, **kwargs):
        """Add the profile to the context."""
        context = super().get_context_data(**kwargs)
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        context['profile'] = profile
        return context

    def form_valid(self, form):
        """Associate the new post with the correct profile."""
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        form.instance.profile = profile

        response = super().form_valid(form)
        files = self.request.FILES.getlist('image_files')
        for file in files:
            Photo.objects.create(post=form.instance, image_file=file)
        return response

    def get_success_url(self):
        """Redirect back to the profile page after creating a post."""
        pk = self.kwargs['pk']
        return reverse('show_profile', kwargs={'pk': pk})

class UpdateProfileView(UpdateView):
    """View for updating an existing Profile."""

    model = Profile
    form_class = UpdateProfileForm
    template_name = "mini_insta/update_profile_form.html"
    context_object_name = "profile"

    def get_success_url(self):
        """Redirect back to the profile page after updating."""
        pk = self.kwargs['pk']
        return reverse('show_profile', kwargs={'pk': pk})
    
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

class PostFeedListView(ListView):
    """Display a feed of posts from profiles that the user follows."""

    model = Post
    template_name = "mini_insta/show_feed.html"
    context_object_name = "posts"

    def get_queryset(self):
        """Return posts from profiles that the user follows."""
        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        return profile.get_post_feed()

class SearchView(ListView):
    """View for searching profiles by username or display name."""

    model = Profile
    template_name = "mini_insta/search_results.html"
    context_object_name = "profiles"

    def dispatch(self, request, *args, **kwargs):
        if 'query' not in self.request.GET:
            pk = self.kwargs['pk'] 
            profile = Profile.objects.get(pk=pk)
            return render(request, 'mini_insta/search.html', {'profile': profile})
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self):
        query = self.request.GET.get('query', '')
        return Post.objects.filter(caption__icontains=query).order_by('-timestamp')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs['pk']
        profile = Profile.objects.get(pk=pk)
        query = self.request.GET.get('query', '')

        if query != '':
            post_results = self.get_queryset()
            profile_results = Profile.objects.filter(username__icontains=query) | Profile.objects.filter(display_name__icontains=query) | Profile.objects.filter(bio_text__icontains=query)

        context['profile'] = profile
        context['query'] = query
        context['post_results'] = post_results
        context['profile_results'] = profile_results
        return context
