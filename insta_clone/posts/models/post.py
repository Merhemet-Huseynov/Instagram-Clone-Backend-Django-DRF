from django.db import models
from django.conf import settings
from posts.validators import validate_image_format, validate_image_size
from typing import Optional


class Post(models.Model):
    """
    Model representing a post made by a user, which includes an image, caption,
    and timestamp. Posts are ordered by creation time with the latest post first.

    Attributes:
        user (ForeignKey): The user who created the post.
        image (ImageField): The image uploaded for the post.
        caption (TextField): The caption associated with the post (optional).
        created_at (DateTimeField): The timestamp when the post was created.
    """
    
    user: models.ForeignKey = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="posts"
    )
    image: models.ImageField = models.ImageField(
        upload_to="posts/", 
        validators=[
            validate_image_format, 
            validate_image_size
        ]  
    )
    caption: Optional[str] = models.TextField(
        blank=True, 
        null=True
    )
    created_at: models.DateTimeField = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        """
        Returns a string representation of the Post instance, including
        the user's email and the first 30 characters of the caption.

        Returns:
            str: A string representation of the post.
        """
        return f"{self.user.email} - {self.caption[:30]}"
   
    def get_like_count(self) -> int:
        """
        Returns the total number of likes on this post.
        """
        return self.likes.count()

    def get_comment_count(self) -> int:
        """
        Returns the total number of comments on this post.
        """
        return self.comments.count()

    def get_users_who_liked(self) -> list:
        """
        Returns a list of emails of users who liked the post.
        """
        return list(self.likes.values_list("user__email", flat=True))
