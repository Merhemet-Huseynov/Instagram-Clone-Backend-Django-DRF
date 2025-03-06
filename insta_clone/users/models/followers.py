from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class Follow(models.Model):
    """
    Model representing a follow relationship between users.
    A user (follower) can follow another user (followed).
    """

    follower = models.ForeignKey(
        User, 
        related_name="following_users", 
        on_delete=models.CASCADE
    )
    followed = models.ForeignKey(
        User, 
        related_name="followers_users",
        on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["follower", "followed"], 
                name="unique_follow"
            )
        ]

    def __str__(self) -> str:
        """Returns a string representation of the follow relationship."""
        return f"{self.follower.username} follows {self.followed.username}"

    def clean(self) -> None:
        """
        Ensures that a user cannot follow themselves.
        Raises:
            ValidationError: If the follower and followed are the same user.
        """
        if self.follower == self.followed:
            raise ValidationError("A user cannot follow themselves.")
        super().clean()

    @classmethod
    def toggle_follow(cls, follower, followed) -> bool:
        """
        Toggles the follow status between two users.
        
        If the follower is not following the followed user, it creates a follow entry.
        If the follower is already following, it removes the follow entry.

        Args:
            follower (User): The user who wants to follow/unfollow.
            followed (User): The user who is being followed/unfollowed.

        Returns:
            bool: True if the follow relationship was created, False if it was removed.
        """
        follow_obj, created = cls.objects.get_or_create(
            follower=follower, 
            followed=followed
        )
        if created:
            return True
        
        follow_obj.delete()  
        return False
