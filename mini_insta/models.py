from django.db import models

# Create your models here.
class Profile(models.Model):
    
    username = models.CharField(blank=True)
    display_name = models.CharField(blank=True)
    profile_image_url = models.URLField(null=True)
    bio_text = models.TextField(blank=True)
    join_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.display_name or self.username