from django.contrib import admin
from ..models import StoryLike
from typing import Type


@admin.register(StoryLike)
class StoryLikeAdmin(admin.ModelAdmin):
    """
    Admin interface for managing StoryLike instances.

    Provides functionality to view, filter, search, and sort story likes.
    """
    
    list_display = (
        "user", 
        "story", 
        "created_at", 
        "is_liked"
    )
    search_fields = (
        "user__email", 
        "story__title"
    )  
    list_filter = (
        "created_at", 
        "story"
    )  
    ordering = (
        "-created_at",
    ) 
    readonly_fields = (
        "created_at",
    )

    def is_liked(self, obj: StoryLike) -> bool:
        """
        Indicates if the story like has been created (liked).
        
        Args:
            obj (StoryLike): The StoryLike object to check.

        Returns:
            bool: True if the like was created, otherwise False.
        """
        return obj.created_at is not None

    is_liked.boolean = True
    is_liked.short_description = "Is Liked?"
