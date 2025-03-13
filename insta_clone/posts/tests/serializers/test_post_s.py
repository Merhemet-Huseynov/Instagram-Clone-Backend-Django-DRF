import pytest
from rest_framework.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.utils.timezone import localtime
from rest_framework.test import APIClient
from django.utils import timezone
from posts.models import Post
from django.contrib.auth import get_user_model
from posts.serializers import PostSerializer


@pytest.mark.django_db
class TestPostSerializer:
    @pytest.fixture
    def user(self) -> get_user_model():
        """
        Fixture to create a user for testing.

        Returns:
            get_user_model(): A user instance.
        """
        return get_user_model().objects.create_user(
            email="testuser@example.com", 
            password="password"
        )

    @pytest.fixture
    def post(self, user) -> Post:
        """
        Fixture to create a post for testing.

        Args:
            user: The user instance used for creating the post.

        Returns:
            Post: A post instance.
        """
        return Post.objects.create(
            user=user,
            image="path/to/image.jpg",
            caption="This is a sample post.",
        )

    def test_post_serializer_valid(self, post: Post) -> None:
        """
        Test the serializer with valid data.

        Args:
            post (Post): The post instance to test the serializer with.
        """
        serializer = PostSerializer(post)
        data = serializer.data

        assert data["id"] == post.id
        assert data["user"] == str(post.user)
        assert data["caption"] == post.caption
        assert data["created_at"] == localtime(post.created_at).strftime("%d %B %Y, %H:%M:%S")

    def test_get_formatted_date(self, post: Post) -> None:
        """
        Test the `get_formatted_date` method.

        Args:
            post (Post): The post instance to test the method with.
        """
        serializer = PostSerializer(post)
        expected_formatted_date = localtime(post.created_at).strftime("%d %B %Y, %H:%M:%S")
        assert serializer.data["created_at"] == expected_formatted_date

    def test_post_creation_timestamp(self, post: Post) -> None:
        """
        Test that the created_at field is set correctly during post creation.

        Args:
            post (Post): The post instance to test the timestamp with.
        """
        assert localtime(post.created_at) <= timezone.now()
