import pytest
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient
from users.models.followers import Follow
from users.models.user import CustomUser
from rest_framework import status
from typing import Dict, Any

from users.serializers.user import (
    UserSerializer, 
    UpdateProfileSerializer
)


@pytest.fixture
def user() -> CustomUser:
    """
    Fixture to create a test user.

    Returns:
        CustomUser: The created user instance.
    """
    return CustomUser.objects.create_user(
        email="testuser@example.com",
        password="testpassword",
        first_name="John",
        last_name="Doe"
    )

@pytest.fixture
def follow(user: CustomUser) -> Follow:
    """
    Fixture to create a follow relationship between two users.

    Args:
        user (CustomUser): The user instance to create a follower for.

    Returns:
        Follow: The created follow relationship instance.
    """
    another_user = CustomUser.objects.create_user(
        email="anotheruser@example.com",
        password="testpassword",
        first_name="Jane",
        last_name="Smith"
    )
    return Follow.objects.create(follower=another_user, followed=user)


@pytest.mark.django_db
class TestUserSerializer:
    def test_user_serializer_fields(self, user: CustomUser, follow: Follow) -> None:
        """
        Test the UserSerializer fields, ensuring it returns the correct data
        including follower and following counts.

        Args:
            user (CustomUser): The user instance to serialize.
            follow (Follow): The follow relationship used to test followers_count.
        """
        serializer = UserSerializer(user)

        data = serializer.data
        assert set(data.keys()) == {
            "email", 
            "bio", 
            "profile_picture", 
            "slug", 
            "followers_count", 
            "following_count"
        }
        assert data["email"] == user.email
        assert data["followers_count"] == 1
        assert data["following_count"] == 0

    def test_get_followers_count(self, user: CustomUser, follow: Follow) -> None:
        """
        Test the followers count method of the UserSerializer.
        """
        serializer = UserSerializer(user)
        assert serializer.data["followers_count"] == 1  

    def test_get_following_count(self, user: CustomUser) -> None:
        """
        Test the following count method of the UserSerializer.
        """
        serializer = UserSerializer(user)
        assert serializer.data["following_count"] == 0  


@pytest.mark.django_db
class TestUpdateProfileSerializer:
    def test_update_profile_serializer_invalid_data(self, user: CustomUser) -> None:
        """
        Test that invalid data (e.g., exceeding max length) raises a validation error.
        """
        data = {
            "first_name": "A" * 31,
        }
        serializer = UpdateProfileSerializer(instance=user, data=data, partial=True)
        assert not serializer.is_valid()
        assert "first_name" in serializer.errors

    def test_update_profile_serializer_partial_update(self, user: CustomUser) -> None:
        """
        Test that partial update works when only some fields are provided.
        """
        data = {"bio": "New bio content."}
        serializer = UpdateProfileSerializer(
            instance=user, 
            data=data, 
            partial=True
        )
        assert serializer.is_valid(), serializer.errors
        updated_user = serializer.save()
        assert updated_user.bio == "New bio content."