from rest_framework import serializers
from likes.models import CommentLike


class CommentLikeSerializer(serializers.ModelSerializer):
    """
    Serializer for the CommentLike model, providing a formatted date field.

    Fields:
        id (int): The unique identifier for the comment like.
        user (str): The user who liked the comment.
        comment (str): The comment that was liked.
        formatted_date (str): The formatted date when the like was created.

    Methods:
        get_formatted_date: Returns the formatted date of the like's creation.
    """

    formatted_date = serializers.SerializerMethodField()

    class Meta:
        model = CommentLike
        fields = [
            "id",
            "user",
            "comment",
            "formatted_date"
        ]
        read_only_fields = [
            "id", 
            "user", 
            "created_at", 
            "formatted_date"
        ]

    def get_formatted_date(self, obj: CommentLike) -> str:
        """
        Returns the formatted creation date of the comment like.

        Args:
            obj (CommentLike): The instance of the CommentLike model.

        Returns:
            str: The formatted date in "YYYY-MM-DD HH:MM:SS" format.
        """
        return obj.created_at.strftime("%Y-%m-%d %H:%M:%S")
