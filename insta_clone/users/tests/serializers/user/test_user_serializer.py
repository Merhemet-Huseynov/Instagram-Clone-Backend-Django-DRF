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
    def test_update_profile_serializer_valid_data(self, user: CustomUser) -> None:
        """
        Test that valid data can successfully update the user profile using PUT method.

        Args:
            user (CustomUser): The user instance to update.
        """
        image = BytesIO()
        image.write(b"image_data") 
        image.seek(0)
        uploaded_file = InMemoryUploadedFile(
            image, None, "test_image.jpg", "image/jpeg", len(image.getvalue()), None
        )

        data = {
            "first_name": "UpdatedFirstName",
            "last_name": "UpdatedLastName",
            "bio": "Updated bio text.",
            "profile_picture": "" 
        }

        client = APIClient()
        client.force_authenticate(user=user)

        response = client.put(f"/api/v1/users/update-profile/", data, format="multipart")

        assert response.status_code == 200
        updated_user = CustomUser.objects.get(id=user.id)
        assert updated_user.first_name == "UpdatedFirstName"
        assert updated_user.last_name == "UpdatedLastName"
        assert updated_user.bio == "Updated bio text."
        assert updated_user.profile_picture == ""

    def test_update_profile_serializer_invalid_data(self, user: CustomUser) -> None:
        """
        Test that invalid data (e.g., exceeding max length) raises a validation error.

        Args:
            user (CustomUser): The user instance to test.
        """
        data = {
            "first_name": "A" * 31, 
        }

        serializer = UpdateProfileSerializer(user, data=data)
        with pytest.raises(ValidationError):
            serializer.is_valid(raise_exception=True)
