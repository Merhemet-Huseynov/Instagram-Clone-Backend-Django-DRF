from rest_framework import serializers
from users.models.followers import Follow


class FollowSerializer(serializers.ModelSerializer):
    """
    Serializer for the Follow model.

    This serializer is used to represent the relationship between 
    a follower and a followed user.
    """

    class Meta:
        model = Follow
        fields = [
            "follower",
            "followed",
            "created_at"
        ]
        read_only_fields: list[str] = [
            "follower",
            "created_at"
        ]
