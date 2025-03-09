from rest_framework import serializers
from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.

    This serializer includes:
    - "user": Read-only field showing the related user's string representation.
    - "formatted_date": A computed field formatting the "created_at" timestamp.
    - Other fields: "id", "image", "caption".

    Read-only fields: "user", "created_at", "formatted_date".
    """

    user: serializers.StringRelatedField = serializers.StringRelatedField(read_only=True)
    formatted_date: serializers.SerializerMethodField = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "user",
            "image",
            "caption",
            "formatted_date",
        ]
        read_only_fields = [
            "user",
            "created_at",
            "formatted_date",
        ]

    def get_formatted_date(self, obj: Post) -> str:
        """
        Returns the formatted creation date of the post.

        Args:
            obj (Post): The post instance.

        Returns:
            str: Formatted date as "DD Month YYYY, HH:MM:SS".
        """
        return obj.created_at.strftime("%d %B %Y, %H:%M:%S")
