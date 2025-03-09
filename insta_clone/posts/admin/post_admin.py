from django.contrib import admin
from django.utils.html import format_html
from ..models import Post
from typing import Any, Tuple


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    Admin interface customization for the Post model. This includes:
    - Displaying user, image preview, caption, and created_at fields in the list view.
    - Adding search functionality for user email and caption.
    - Enabling filtering by creation date.
    - Paginating the list with 20 entries per page.
    - Ordering posts by creation date in descending order.
    """

    list_display = (
        "user", 
        "image_preview",
        "caption", 
        "created_at",
        "short_caption"
    )
    search_fields = (
        "user__email", 
        "caption"
    )
    list_filter = (
        "created_at",
    )
    list_per_page = 20
    ordering = (
        "-created_at",
    )
    
    def image_preview(self, obj: Post) -> str:
        """
        Display a small preview of the post's image in the admin interface.
        
        Args:
            obj: The Post model instance.
        
        Returns:
            HTML string to render image or a placeholder text if no image is present.
        """
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return "No Image"
    image_preview.short_description = "Image Preview"

    def short_caption(self, obj: Post) -> str:
        """
        Display a truncated version of the post's caption.
        
        Args:
            obj: The Post model instance.
        
        Returns:
            A shortened caption (first 30 characters) or "No Caption" if none is provided.
        """
        return obj.caption[:30] + "..." if obj.caption else "No Caption"
    short_caption.short_description = "Short Caption"

    def get_search_results(
        self, request: Any, queryset: Any, search_term: str
    ) -> Tuple[Any, bool]:
        """
        Customize the search results to filter by caption containing the search term.
        
        Args:
            request: The HTTP request object.
            queryset: The queryset of Post model.
            search_term: The term to search for in captions.
        
        Returns:
            A tuple containing the filtered queryset and a boolean indicating if distinct results are needed.
        """
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset.filter(caption__icontains=search_term), use_distinct
