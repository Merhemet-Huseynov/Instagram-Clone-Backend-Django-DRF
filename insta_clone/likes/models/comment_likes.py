from django.db import models
from django.conf import settings


class CommentLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="comment_likes"
    )
    comment = models.ForeignKey(
        "comments.Comment", 
        on_delete=models.CASCADE, 
        related_name="likes"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "comment"], 
                name="unique_user_comment_like"
            )
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.email} liked comment {self.comment.id}"

    @classmethod
    def toggle_like(cls, user: settings.AUTH_USER_MODEL, comment: "comments.Comment") -> bool:
        """
        Toggles the like status for a comment.

        If the user has not liked the comment, it creates a like entry.
        If the user has already liked the comment, it removes the like entry.

        Returns:
            bool: True if the like was created, False if it was removed.
        """
        like_obj, created = cls.objects.get_or_create(user=user, comment=comment)
        if created:
            return True

        like_obj.delete()
        return False
