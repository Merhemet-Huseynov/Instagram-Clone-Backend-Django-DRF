from django.db import models
from django.conf import settings
from posts.models import Post
from typing import Type


class PostLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="likes"
    )
    post = models.ForeignKey(
        Post, 
        on_delete=models.CASCADE, 
        related_name="likes"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("user", "post") 
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.user.email} liked {self.post.id}"

    @classmethod
    def toggle_like(cls: Type["PostLike"], user: settings.AUTH_USER_MODEL, post: Post) -> bool:
        """
        Toggles the like status for a post by a user.
        
        If the user has not liked the post, it creates a like entry.
        If the user has already liked the post, it removes the like entry.

        Args:
            user (User): The user who wants to like/unlike the post.
            post (Post): The post that is being liked/unliked.

        Returns:
            bool: True if the like was created, False if it was removed.
        """
        like_obj, created = cls.objects.get_or_create(
            user=user,
            post=post
        )
        if created:
            return True
        
        like_obj.delete()
        return False
