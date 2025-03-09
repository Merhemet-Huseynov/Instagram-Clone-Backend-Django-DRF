import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from typing import Tuple

CustomUser = get_user_model()

@pytest.fixture
def create_user(db) -> CustomUser:
    """Creates a test user.

    Args:
        db: The test database setup provided by pytest.

    Returns:
        CustomUser: The created user.
    """
    return CustomUser.objects.create_user(
        email="testuser@example.com",
        password="securepassword123",
        first_name="Test",
        last_name="User"
    )

@pytest.fixture
def authenticated_client(create_user: CustomUser) -> Tuple[APIClient, CustomUser]:
    """Returns an authenticated API client with the test user.

    Args:
        create_user (CustomUser): The user to authenticate.

    Returns:
        Tuple[APIClient, CustomUser]: A tuple containing the authenticated client and the user.
    """
    client = APIClient()
    client.force_authenticate(user=create_user)
    return client, create_user

@pytest.mark.django_db
def test_user_profile_view(authenticated_client: Tuple[APIClient, CustomUser]) -> None:
    """Tests the successful retrieval of the user profile.

    Args:
        authenticated_client (Tuple[APIClient, CustomUser]): The authenticated client and the user.

    Asserts:
        - The status code is 200.
        - The response data matches the user's email, bio, followers count, and following count.
    """
    client, user = authenticated_client
    url = reverse("user-profile", kwargs={"username": user.slug})
    
    response = client.get(url)

    assert response.status_code == 200
    assert response.data["email"] == user.email
    assert response.data["bio"] == user.bio
    assert response.data["followers_count"] == 0
    assert response.data["following_count"] == 0

@pytest.mark.django_db
def test_update_profile_view(authenticated_client: Tuple[APIClient, CustomUser]) -> None:
    """Tests the successful update of the user profile (multipart/form-data).

    Args:
        authenticated_client (Tuple[APIClient, CustomUser]): The authenticated client and the user.

    Asserts:
        - The status code is 200.
        - The response data matches the updated user information.
        - The user's data in the database is updated.
    """
    client, user = authenticated_client
    url = reverse("update-profile")

    updated_data = {
        "first_name": "Updated",
        "last_name": "User",
        "bio": "This is an updated bio",
    }

    response = client.put(url, updated_data, format="multipart")

    assert response.status_code == 200
    assert response.data["first_name"] == updated_data["first_name"]
    assert response.data["last_name"] == updated_data["last_name"]
    assert response.data["bio"] == updated_data["bio"]

    user.refresh_from_db()
    assert user.first_name == updated_data["first_name"]
    assert user.last_name == updated_data["last_name"]
    assert user.bio == updated_data["bio"]