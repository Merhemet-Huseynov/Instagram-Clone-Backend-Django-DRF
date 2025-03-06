from typing import Any
from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth import get_user_model
from ..models import Follow

User = get_user_model()


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """
    Admin class for managing the Follow model in the Django admin panel.
    """

    model = Follow
    list_display = (
        "follower", 
        "followed", 
        "created_at", 
        "followed_since"
    )
    list_filter = ("created_at",)
    search_fields = (
        "follower__email", 
        "followed__email", 
        "follower__username", 
        "followed__username"
    )
    ordering = ("-created_at",)
    list_select_related = ("follower", "followed")
    date_hierarchy = "created_at"
    readonly_fields = ("created_at",)

    def followed_since(self, obj: Follow) -> str:
        """
        Returns the formatted date and time when the user started following another user.

        Args:
            obj (Follow): The Follow object.

        Returns:
            str: Formatted date and time (YYYY-MM-DD HH:MM).
        """
        return format_html("<span>{}</span>", obj.created_at.strftime("%Y-%m-%d %H:%M"))
    
    followed_since.short_description = "Followed Since"

    def get_queryset(self, request: Any) -> Any:
        """
        Optimizes the queryset by using `select_related` to prefetch related fields.

        Args:
            request (Any): The Django admin request.

        Returns:
            QuerySet: Optimized queryset for the Follow model.
        """
        queryset = super().get_queryset(request)
        return queryset.select_related("follower", "followed")
