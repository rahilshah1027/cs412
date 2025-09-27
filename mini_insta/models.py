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