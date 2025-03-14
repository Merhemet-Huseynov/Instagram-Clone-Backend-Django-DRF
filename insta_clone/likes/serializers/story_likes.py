from rest_framework import serializers
from likes.models import StoryLike


class StoryLikeSerializer(serializers.ModelSerializer):
    """
    Serializer for the StoryLike model.

    This serializer transforms StoryLike model instances into JSON format,
    including user, story, and creation timestamp (created_at).
    The created_at field is formatted as "YYYY-MM-DD HH:MM:SS" for better readability.
    """

    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    class Meta:
        model = StoryLike
        fields = [
            "id",
            "user",
            "story",
            "created_at"
        ]
        read_only_fields = [
            "id", 
            "user", 
            "story",
            "created_at"
        ]
