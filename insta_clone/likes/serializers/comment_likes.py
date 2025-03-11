from rest_framework import serializers
from likes.models import CommentLike


class CommentLikeSerializer(serializers.ModelSerializer):
    """
    Serializer for the CommentLike model.

    This serializer is responsible for transforming CommentLike model instances
    into JSON format, including user, comment, and creation timestamp (created_at).
    The created_at field is formatted as "YYYY-MM-DD HH:MM:SS" for better readability.
    """

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = CommentLike
        fields = [
            "id",
            "user",
            "comment",
            "created_at"
        ]
        read_only_fields = [
            "id", 
            "user", 
            "comment",
            "created_at"
        ]
        