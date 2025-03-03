from django.contrib import admin
from ..models import Follow
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    """
    Admin panel customization for Follow model.
    
    This class customizes the display and behavior of the Follow model
    in the Django admin panel. It adds search functionality, filters,
    ordering, and date hierarchy for better usability.
    """
    
    list_display = ("follower", "followed", "created_at")
    search_fields = ("follower__username", "followed__username")  
    list_filter = ("created_at",)  
    ordering = ("-created_at",)  
    date_hierarchy = "created_at"  
    
    def get_queryset(self, request: 'HttpRequest') -> 'QuerySet[Follow]':
        """
        Custom queryset to order the follow records by the most recent creation.
        
        Args:
            request (HttpRequest): The HTTP request object.
        
        Returns:
            QuerySet[Follow]: The queryset of follow records ordered by creation date.
        """
        qs = super().get_queryset(request)
        return qs.order_by("-created_at")
