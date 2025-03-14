from django.contrib import admin
from django.utils.html import format_html
from ..models import Story
from typing import Any


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = (
        "user", 
        "created_at", 
        "expires_at", 
        "is_expired", 
        "image_preview", 
        "video_preview"
    )
    search_fields = (
        "user__email",
    )
    list_filter = (
        "created_at", 
        "expires_at"
    )

    def image_preview(self, obj: Story) -> str:
        """
        Display image preview in the admin panel.

        Args:
            obj (Story): The Story object for which the image 
            preview is being generated.

        Returns:
            str: HTML representation of the image or a placeholder ('-') 
            if no image is available.
        """
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: cover;" />', 
                obj.image.url
            )
        return "-"
    image_preview.short_description = "Image Preview"

    def video_preview(self, obj: Story) -> str:
        """
        Display video preview in the admin panel.

        Args:
            obj (Story): The Story object for which the video 
            preview is being generated.

        Returns:
            str: HTML representation of the video or a placeholder ('-') 
            if no video is available.
        """
        if obj.video:
            return format_html(
                '<video width="150" height="100" controls>'
                '<source src="{}" type="video/mp4">'
                "Your browser does not support the video tag.</video>",
                obj.video.url
            )
        return "-"
    video_preview.short_description = "Video Preview"

    def get_queryset(self, request: Any) -> "QuerySet":
        """
        Return the queryset of Story objects with related user data 
        for better query optimization.

        Args:
            request (Any): The request object passed by the Django admin.

        Returns:
            QuerySet: The optimized queryset with related user data.
        """
        queryset = super().get_queryset(request)
        return queryset.select_related("user")
