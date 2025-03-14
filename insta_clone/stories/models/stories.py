from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class Story(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="stories"
    )
    image = models.ImageField(
        upload_to="stories/images/", 
        blank=True, 
        null=True
    )
    video = models.FileField(
        upload_to="stories/videos/", 
        blank=True, 
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs) -> None:
        """
        Sets the "expires_at" field to 24 hours after creation 
        if it's not already set.
        The story will automatically expire after 24 hours.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            None
        """
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(hours=24)
        super().save(*args, **kwargs)

    @property
    def is_expired(self) -> bool:
        """
        Checks if the story has expired based on the current 
        time and the "expires_at" field.

        Returns:
            bool: True if the story is expired, False otherwise.
        """
        return timezone.now() >= self.expires_at

    def __str__(self) -> str:
        """
        Returns a string representation of the story, 
        including the user's email and the story's creation time.

        Returns:
            str: A string representation of the story.
        """
        return f"{self.user.email} - {self.created_at}"

    def get_like_count(self) -> int:
        """
        Returns the total number of likes on this story.

        Returns:
            int: The number of likes on the story.
        """
        return self.likes.count()
