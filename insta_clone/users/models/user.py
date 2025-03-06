from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.managers import CustomUserManager
from utils.slug_manager import generate_unique_slug


class CustomUser(AbstractUser):
    """
    Custom user model that uses email as the unique identifier instead of username.
    """

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
    slug = models.SlugField(
        unique=True,
        blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        """
        Returns the string representation of the user.
        """
        return self.email

    def save(self, *args, **kwargs) -> None:
        """
        Generates a unique slug for the user if it's not set.
        Uses the full name if available, otherwise derives from the email.
        """
        if not self.slug:
            full_name = f"{self.first_name} {self.last_name}".strip()
            if not full_name:
                full_name = self.email.split("@")[0]
            self.slug = generate_unique_slug(full_name, CustomUser)
        super().save(*args, **kwargs)
