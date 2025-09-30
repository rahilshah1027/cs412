"""Models for the mini_insta app."""
from django.db import models

class Profile(models.Model):
    """A public user profile.

    Attributes:
        username
        display_name
        profile_image_url
        bio_text
        join_date
    """

    # Short user handle
    username = models.CharField(blank=True)
    # Display name shown to other user
    display_name = models.CharField(blank=True)
    # Avatar image URL
    profile_image_url = models.URLField(null=True)
    # Optional longer bio/description
    bio_text = models.TextField(blank=True)
    # Auto-updated date field (set to now on each save)
    join_date = models.DateField(auto_now=True)

    def __str__(self):
        """Return a readable identifier for the profile.

        Prefer display_name, otherwise return username.
        """
        return self.display_name or self.username

    def get_all_posts(self):
        """Return all posts made by this profile."""
        return Post.objects.filter(profile=self).order_by('-timestamp')


class Post(models.Model):
    """A post made by a user.

    Attributes:
        profile
        caption
        timestamp
    """

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    caption = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a readable identifier for the post."""
        return f"Post by {self.profile} at {self.timestamp}"
    
    def get_all_photos(self):
        """
        Return all Photo objects related to this Post.
        """
        return Photo.objects.filter(post=self)


class Photo(models.Model):
    """A photo associated with a post.

    Attributes:
        post
        image_url
        timestamp
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    image_url = models.URLField(null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a readable identifier for the photo."""
        return f"Photo for post {self.post.id} at {self.image_url}"