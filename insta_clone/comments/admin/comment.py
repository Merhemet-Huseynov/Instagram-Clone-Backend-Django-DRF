from django.contrib import admin
from ..models import Comment
from likes.models import CommentLike
from typing import List


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "user", 
        "post", 
        "text", 
        "created_at", 
        "like_count"
    )  
    list_filter = (
        "post", 
        "created_at"
    ) 
    search_fields = (
        "user__email", 
        "text"
    ) 
    ordering = (
        "-created_at",
    ) 
    actions = [
        "delete_selected"
    ]  

    def like_count(self, obj: Comment) -> int:
        """
        Returns the like count for the comment.

        Parameters:
        obj (Comment): The comment instance for which to calculate the like count.

        Returns:
        int: The number of likes for the comment.
        """
        return CommentLike.objects.filter(comment=obj).count()
    like_count.short_description = "Like Count"

    def get_users_who_liked(self, obj: Comment) -> str:
        """
        Returns the email addresses of users who liked the comment.

        Parameters:
        obj (Comment): The comment instance for which to retrieve users who liked it.

        Returns:
        str: A comma-separated string of email addresses of users who liked the comment.
        """
        return ", ".join([user.email for user in obj.get_users_who_liked()])
    get_users_who_liked.short_description = "Users Who Liked"