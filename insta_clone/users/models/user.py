from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.managers import CustomUserManager


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(
        _("email address"), 
        unique=True
    )
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", 
        blank=True, 
        null=True
    )   
    bio = models.TextField(
        blank=True, 
        null=True
    )


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email