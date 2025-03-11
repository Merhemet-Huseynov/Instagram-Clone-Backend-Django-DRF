from django.db import models
from django.conf import settings
from likes.models.comment_likes import CommentLike
from typing import List


class Comment(models.Model):
    post = models.ForeignKey(
        "posts.Post", 
        on_delete=models.CASCADE, 
        related_name="comments"
    ) 
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE
    )
    text = models.TextField()
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-created_at"]  
    
    def __str__(self) -> str:
        """
        Returns a string representation of the comment, showing the user's email 
        and the first 30 characters of the text.
        """
        return f"{self.user.email} - {self.text[:30]}" 
    
    def get_like_count(self) -> int:
        """
        Returns the count of likes for the comment.

        Returns:
            int: The number of likes on the comment.
        """
        return CommentLike.objects.filter(comment=self).count()

    def get_users_who_liked(self) -> List[int]:
        """
        Returns a list of user IDs who liked the comment.

        Returns:
            List[int]: A list of user IDs who have liked the comment.
        """
        return list(CommentLike.objects.filter(comment=self).values_list("user", flat=True))
