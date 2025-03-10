from django.contrib import admin
from ..models import CommentLike
from typing import Any


@admin.register(CommentLike)
class CommentLikeAdmin(admin.ModelAdmin):
    """
    Admin interface for managing CommentLike instances.

    Provides functionality to list, filter, search, and delete selected comment likes.
    """
    list_display = ("user", "comment", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__email", "comment__text")

    actions = ["remove_likes"]

    def remove_likes(self, request: Any, queryset: Any) -> None:
        """
        Removes selected comment likes from the database.

        Args:
            request: The HTTP request object.
            queryset: The set of CommentLike objects to delete.
        """
        queryset.delete()
        self.message_user(request, "Selected comment likes were deleted.")
    
    remove_likes.short_description = "Delete selected likes"
