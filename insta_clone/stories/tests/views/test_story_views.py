import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from datetime import timedelta
from django.utils import timezone
from typing import Any

from stories.models import Story
from users.models import Follow


@pytest.fixture
def user() -> Any:
    """Create a user for testing.

    Returns:
        user: The created test user.
    """
    user_model = get_user_model()
    user = user_model.objects.create_user(
        email="testuser@example.com",
        password="password123"
    )
    return user

@pytest.fixture
def followed_user() -> Any:
    """Create a followed user for testing.

    Returns:
        followed_user: The created followed user.
    """
    user_model = get_user_model()
    user = user_model.objects.create_user(
        email="followeduser@example.com",
        password="password123"
    )
    return user

@pytest.fixture
def api_client() -> APIClient:
    """Create an APIClient for testing.

    Returns:
        APIClient: The created APIClient instance.
    """
    return APIClient()

@pytest.mark.django_db
def test_create_story(api_client: APIClient, user: Any) -> None:
    """Test creating a new story.

    Args:
        api_client: The APIClient used for making requests.
        user: The user creating the story.
    """
    api_client.force_authenticate(user=user)
    data = {
        "image": "",
        "video": "",
    }

    response = api_client.post(
        "/api/v1/stories/", 
        data, 
        format="multipart"
    )

    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.data
    assert response.data["user"] == user.email

@pytest.mark.django_db
def test_create_story_unauthenticated(api_client: APIClient) -> None:
    """Test attempting to create a story without authentication.

    Args:
        api_client: The APIClient used for making requests.
    """
    data = {
        "image": "",
        "video": "",
    }

    response = api_client.post(
        "/api/v1/stories/",
        data, 
        format="multipart"
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_get_active_stories(api_client: APIClient, user: Any, followed_user: Any) -> None:
    """Test retrieving active stories from followed users.

    Args:
        api_client: The APIClient used for making requests.
        user: The user who follows other users.
        followed_user: The user who creates the stories.
    """

    Follow.objects.create(
        follower=user, 
        followed=followed_user
    )

    story = Story.objects.create(
        user=followed_user,
        image="dummy_image_path.jpg",
        expires_at=timezone.now() + timedelta(hours=1)
    )

    api_client.force_authenticate(user=user)
    response = api_client.get("/api/v1/stories/active/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["id"] == story.id

@pytest.mark.django_db
def test_get_active_stories_no_followed_users(api_client: APIClient, user: Any) -> None:
    """Test retrieving active stories when the user has no followed users.

    Args:
        api_client: The APIClient used for making requests.
        user: The user with no followed users.
    """
    api_client.force_authenticate(user=user)
    response = api_client.get("/api/v1/stories/active/")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 0
