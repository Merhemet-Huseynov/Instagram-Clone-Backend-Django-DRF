from rest_framework import serializers
from comments.models import Comment
from typing import List, Dict


class CommentSerializer(serializers.ModelSerializer):
    users_who_liked = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    like_count = serializers.IntegerField(
        source="get_like_count", 
        read_only=True
    )
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", 
        read_only=True
    )
    post = serializers.SerializerMethodField()  

    class Meta:
        model = Comment
        fields = [
            "id", 
            "post",  
            "user", 
            "text", 
            "created_at", 
            "like_count", 
            "users_who_liked"
        ]
        read_only_fields = ["id"] 

    def get_user(self, obj: Comment) -> Dict[str, str]:
        """
        Returns the data of the user who made the comment.

        Args:
            obj (Comment): The comment object.

        Returns:
            dict: A dictionary containing the user's ID and email.
        """
        return {
            "id": obj.user.id,
            "email": obj.user.email,
            "name": obj.user.get_full_name() 
        }

    def get_users_who_liked(self, obj: Comment) -> List[str]:
        """
        Returns a list of emails of users who liked the comment.

        Args:
            obj (Comment): The comment object.

        Returns:
            list: A list of emails of users who liked the comment.
        """
        liked_users = obj.get_users_who_liked() 
        users = obj.user.__class__.objects.filter(id__in=liked_users)  
        return [user.email for user in users]

    def get_post(self, obj: Comment) -> Dict[str, str]:
        """
        Returns the post's image and caption for the given comment.

        Args:
            obj (Comment): The comment object.

        Returns:
            dict: A dictionary containing the post's image and caption.
        """
        if obj.post:
            return {
                "image": obj.post.image.url if obj.post.image else None, 
                "caption": obj.post.caption
            }
        return {}

    def validate_text(self, value: str) -> str:
        """
        Validates that the comment text is not empty.

        Args:
            value (str): The comment text.

        Returns:
            str: The validated comment text.

        Raises:
            serializers.ValidationError: If the comment text is empty or only 
            contains whitespace.
        """
        if not value.strip():
            raise serializers.ValidationError("Comment text cannot be empty.")
        return value
