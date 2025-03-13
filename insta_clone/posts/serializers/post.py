from django.utils.timezone import localtime
from rest_framework import serializers
from posts.models import Post

class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.

    This serializer includes:
    - "user": Read-only field showing the related user's string representation.
    - "created_at": Automatically formatted timestamp.
    - "like_count": Number of likes on the post.
    - "comment_count": Number of comments on the post.
    - "users_who_liked": List of users who liked the post.
    """

    user = serializers.StringRelatedField(
        read_only=True
    )
    created_at = serializers.SerializerMethodField()
    like_count = serializers.IntegerField(
        source="get_like_count", 
        read_only=True
    )
    comment_count = serializers.IntegerField(
        source="get_comment_count", 
        read_only=True
    )
    users_who_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "image",
            "caption",
            "created_at",
            "like_count",
            "comment_count",
            "users_who_liked",
        ]
        read_only_fields = [
            "user",
            "created_at",
            "like_count",
            "comment_count",
            "users_who_liked",
        ]

    def get_created_at(self, obj: Post) -> str:
        """
        Returns the formatted created_at timestamp in the Asia/Baku timezone.

        Args:
            obj (Post): The post instance.

        Returns:
            str: Formatted timestamp.
        """
        return localtime(obj.created_at).strftime("%d %B %Y, %H:%M:%S")

    def get_users_who_liked(self, obj: Post) -> list:
        """
        Returns a list of emails of users who liked the post.

        Args:
            obj (Post): The post instance.

        Returns:
            list: A list of emails of users who liked the post.
        """
        return obj.likes.values_list("user__email", flat=True)
