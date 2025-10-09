"""Views for the mini_insta app."""


from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView
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
        # image_url = self.request.POST.get('image_url')
        # print("Image URL:", image_url)  # Debugging line
        # if image_url:
        #     Photo.objects.create(post=form.instance, image_url=image_url)
        files = self.request.FILES.getlist('image_files')
        print("Uploaded files:", files)  # Debugging line
        for file in files: # ASK IN CLASS ON THURSDAY (THUMBNAIL OF POST WONT SHOW PHOTO)
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