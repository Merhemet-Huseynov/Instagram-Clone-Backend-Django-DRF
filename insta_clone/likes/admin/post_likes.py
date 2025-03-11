from django.contrib import admin
from ..models import PostLike
from typing import List


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Like model.
    Provides features like listing, filtering, and searching for likes.
    Also allows bulk deletion of likes from the admin interface.
    """
    list_display = ("user", "post", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__email", "post__title")

    actions = ["remove_likes"]

    def remove_likes(self, request, queryset) -> None:
        """
        Custom action to delete selected likes in bulk.
        
        This action is available from the Django admin interface.
        
        Args:
            request (HttpRequest): The request object.
            queryset (QuerySet): A queryset of selected Like objects.
        """
        queryset.delete()
        self.message_user(request, "Selected likes were deleted.")

    remove_likes.short_description = "Delete selected likes"
