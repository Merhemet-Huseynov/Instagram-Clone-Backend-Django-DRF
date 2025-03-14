from django.db import models
from django.conf import settings
from stories.models import Story
from typing import Type


class StoryLike(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name="story_likes"
    )
    story = models.ForeignKey(
        Story, 
        on_delete=models.CASCADE, 
        related_name="likes"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        unique_together = ("user", "story") 
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.user.email} liked story {self.story.id}"

    @classmethod
    def toggle_like(cls: Type["StoryLike"], 
                    user: settings.AUTH_USER_MODEL, 
                    story: Story) -> bool:
        """
        Toggles the like status for a story by a user.
        
        If the user has not liked the story, it creates a like entry.
        If the user has already liked the story, it removes the like entry.

        Args:
            user (User): The user who wants to like/unlike the story.
            story (Story): The story that is being liked/unliked.

        Returns:
            bool: True if the like was created, False if it was removed.
        """
        like_obj, created = cls.objects.get_or_create(
            user=user,
            story=story
        )
        if created:
            return True
        
        like_obj.delete()
        return False
