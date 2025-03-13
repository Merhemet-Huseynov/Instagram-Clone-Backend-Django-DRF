from rest_framework import serializers
from likes.models import PostLike


class PostLikeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Like model, including fields for the like's ID, user, 
    associated post, and formatted creation date. It also includes a method 
    for formatting the date when the like was created.
    """

    formatted_date = serializers.SerializerMethodField()

    class Meta:
        model = PostLike
        fields = [
            "id", 
            "user", 
            "post", 
            "formatted_date"
        ]
        read_only_fields = [
            "id", 
            "user", 
            "created_at",
            "formatted_date",
        ]

    def get_formatted_date(self, obj):
        """
        Returns a formatted string representation of the like's creation date.

        Args:
            obj (PostLike): The instance of the PostLike model.

        Returns:
            str: A string formatted date of the like's creation.
        """
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
