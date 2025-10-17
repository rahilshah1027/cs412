"""Models for the mini_insta app."""
from django.db import models
from django.urls import reverse

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
    
    def get_followers(self):
        """Return all profiles that follow this profile."""
        followers = Follow.objects.filter(follower_profile=self)
        return [follower.profile for follower in followers]

    def get_num_followers(self):
        """Return the number of followers this profile has."""
        return len(self.get_followers())
    
    def get_following(self):
        """Return all profiles that this profile is following."""
        following = Follow.objects.filter(profile=self)
        return [follow.follower_profile for follow in following]
    
    def get_num_following(self):
        """Return the number of profiles this profile is following."""
        return len(self.get_following())

    def get_post_feed(self):
        """Return a list of posts made by this profile and profiles they follow."""
        followed_profiles = self.get_following()
        posts = Post.objects.filter(profile__in=followed_profiles).order_by('-timestamp')
        return posts

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

    def get_absolute_url(self):
        """Return the absolute URL to view this post."""
        return reverse("show_post", kwargs={"pk": self.pk})

    def get_all_comments(self):
        """Return all comments made on this post."""
        return Comment.objects.filter(post=self).order_by('timestamp')

    def get_likes(self):
        """Return all likes made on this post."""
        return Like.objects.filter(post=self)
    
    def get_num_likes(self):
        """Return the number of likes on this post."""
        return self.get_likes().count()

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
    image_file = models.ImageField(blank=True)

    def __str__(self):
        """Return a readable identifier for the photo."""
        if self.image_file:
            return f"Photo for post {self.post.id} at: {self.image_file.url}"
        elif self.image_url:
            return f"Photo for post {self.post.id} at URL: {self.image_url}"
        else:
            return f"Photo for post {self.post.id} (no image available)"
    
    def get_image_url(self):
        """Return the image URL, preferring uploaded file if available."""
        if self.image_file:
            return self.image_file.url
        return self.image_url
    
class Follow(models.Model):
    """A following relationship between two profiles.

    Attributes:
        profile
        follower_profile
        timestamp
    """

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='profile')
    follower_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='follower_profile')
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a readable identifier for the follow relationship."""
        return f"{self.profile} follows {self.follower_profile}"
    

class Comment(models.Model):
    """A comment made on a post.

    Attributes:
        post
        profile
        timestamp
        text
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    text = models.TextField()

    def __str__(self):
        """Return a readable identifier for the comment."""
        return f"Comment by {self.profile} on {self.post} at {self.timestamp}"
    
class Like(models.Model):
    """A like made on a post.

    Attributes:
        post
        profile
        timestamp
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a readable identifier for the like."""
        return f"Liked by {self.profile} on {self.post} at {self.timestamp}"