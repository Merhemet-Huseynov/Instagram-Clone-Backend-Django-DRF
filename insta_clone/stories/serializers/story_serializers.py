from rest_framework import serializers
from stories.models import Story
from django.db.models import Count
from django.utils.timezone import localtime
from typing import List


class StorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(
        read_only=True
    )
    like_count = serializers.IntegerField(
        source="get_like_count", 
        read_only=True
    )
    created_at = serializers.SerializerMethodField()
    expires_at = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()
    liked_users = serializers.SerializerMethodField()

    class Meta:
        model = Story
        fields = [
            "id",
            "user",
            "image",
            "video",
            "created_at",
            "expires_at",
            "is_expired",
            "like_count",
            "liked_users",
        ]
        read_only_fields = [
            "user",
            "created_at",
            "expires_at",
            "is_expired",
            "like_count",
            "liked_users",
        ]

    def get_created_at(self, obj: Story) -> str:
        """
        Returns the formatted creation date of the story in local time.

        Args:
            obj (Story): The story object.

        Returns:
            str: The formatted creation date.
        """
        return localtime(obj.created_at).strftime("%d %B %Y, %H:%M:%S")

    def get_expires_at(self, obj: Story) -> str:
        """
        Returns the formatted expiration date of the story in local time.

        Args:
            obj (Story): The story object.

        Returns:
            str: The formatted expiration date.
        """
        return localtime(obj.expires_at).strftime("%d %B %Y, %H:%M:%S")

    def get_is_expired(self, obj: Story) -> bool:
        """
        Returns whether the story has expired.

        Args:
            obj (Story): The story object.

        Returns:
            bool: True if the story is expired, otherwise False.
        """
        return obj.is_expired

    def get_liked_users(self, obj: Story) -> List[str]:
        """
        Returns a list of emails of users who liked the story.

        Args:
            obj (Story): The story object.

        Returns:
            list: A list of email addresses of users who liked the story.
        """
        return list(obj.likes.values_list("user__email", flat=True))
