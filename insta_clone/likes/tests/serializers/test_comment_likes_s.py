import pytest
from rest_framework.exceptions import ValidationError
from likes.models import CommentLike
from posts.models import Post
from comments.models import Comment
from django.contrib.auth import get_user_model
from rest_framework.utils import json
from likes.serializers import CommentLikeSerializer


@pytest.mark.django_db
class TestCommentLikeSerializer:
    
    @pytest.fixture
    def user(self) -> get_user_model():
        """
        Fixture to create a user for testing purposes.

        Returns:
            get_user_model(): The created user object.
        """
        return get_user_model().objects.create_user(
            email="user@example.com", 
            password="testpassword"
        )

    @pytest.fixture
    def post(self, user) -> Post:
        """
        Fixture to create a post for testing purposes.

        Args:
            user (get_user_model()): The user who creates the post.

        Returns:
            Post: The created post object.
        """
        return Post.objects.create(
            user=user, 
            image="test_image.jpg"
        )

    @pytest.fixture
    def comment(self, post, user) -> Comment:
        """
        Fixture to create a comment for testing purposes.

        Args:
            post (Post): The post on which the comment is made.
            user (get_user_model()): The user who creates the comment.

        Returns:
            Comment: The created comment object.
        """
        return Comment.objects.create(
            post=post, 
            user=user, 
            text="This is a comment"
        )

    @pytest.fixture
    def comment_like(self, comment, user) -> CommentLike:
        """
        Fixture to create a like for a comment.

        Args:
            comment (Comment): The comment being liked.
            user (get_user_model()): The user who likes the comment.

        Returns:
            CommentLike: The created CommentLike object.
        """
        return CommentLike.objects.create(user=user, comment=comment)

    def test_comment_like_serializer_valid(self, comment_like: CommentLike) -> None:
        """
        Test that the CommentLikeSerializer returns the correct data for a valid CommentLike object.

        Args:
            comment_like (CommentLike): The CommentLike object to serialize.
        """
        serializer = CommentLikeSerializer(instance=comment_like)
        data = serializer.data
        assert data["user"] == comment_like.user.id
        assert data["comment"] == comment_like.comment.id
        assert "created_at" in data

    def test_comment_like_serializer_invalid(self) -> None:
        """
        Test that CommentLikeSerializer does not accept input data.

        Ensures the serializer fails when invalid data is provided (read-only fields).
        """
        invalid_data = {
            "user": None,  
            "comment": None,  
        }
        serializer = CommentLikeSerializer(data=invalid_data)

        assert not serializer.is_valid()

    def test_toggle_like(self, user: get_user_model(), comment: Comment) -> None:
        """
        Test that the toggle_like method correctly creates and deletes a like.

        Args:
            user (get_user_model()): The user performing the like toggle.
            comment (Comment): The comment to be liked/unliked.
        """
 
        like_created = CommentLike.toggle_like(user, comment)
        assert like_created is True
        assert CommentLike.objects.filter(user=user, comment=comment).exists() is True

        like_created = CommentLike.toggle_like(user, comment)
        assert like_created is False
        assert CommentLike.objects.filter(user=user, comment=comment).exists() is False
