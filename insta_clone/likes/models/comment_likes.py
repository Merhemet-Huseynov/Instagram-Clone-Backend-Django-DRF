from django.db import models
from django.conf import settings
from posts.models import Post
from comments.models import Comment


class CommentLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="comment_likes"
    )
    comment = models.ForeignKey(
        Comment, 
        on_delete=models.CASCADE, 
        related_name="likes"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("user", "comment")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} liked comment {self.comment.id}"

    @classmethod
    def toggle_like(cls, user: settings.AUTH_USER_MODEL, comment: Comment) -> bool:
        """
        Toggles the like status for a comment.

        If the user has not liked the comment, it creates a like entry.
        If the user has already liked the comment, it removes the like entry.

        Args:
            user (User): The user who wants to like/unlike the comment.
            comment (Comment): The comment that is being liked/unliked.

        Returns:
            bool: True if the like was created, False if it was removed.
        """
        like_obj, created = cls.objects.get_or_create(
            user=user,
            comment=comment
        )
        if created:
            return True
        
        like_obj.delete()
        return False