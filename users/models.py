from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """
    Extends Django's default User model with additional fields.
    
    Attributes:
        profile_picture (ImageField): Stores the user's profile picture. Optional.
        bio (TextField): A short biography or description. Max 500 chars. Optional.
    """
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True)
    
    def __str__(self):
        """String representation of the user (their username)."""
        return self.username