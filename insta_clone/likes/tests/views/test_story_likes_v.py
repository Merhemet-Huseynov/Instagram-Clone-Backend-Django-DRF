import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model
from django.urls import reverse
from unittest import mock

from stories.models import Story
from likes.models import StoryLike


@pytest.mark.django_db
class TestStoryLikeToggleAPIView:
    """Test suite for the Story Like Toggle API view."""

    @pytest.fixture
    def user(self) -> get_user_model():
        """Create a test user."""
        user = get_user_model().objects.create_user(
            email="testuser@example.com",
            password="password123"
        )
        return user

    @pytest.fixture
    def story(self, user: get_user_model()) -> Story:
        """Create a test story for the user."""
        story = Story.objects.create(
            user=user,
            created_at="2025-03-15T12:00:00Z",
            expires_at="2025-03-16T12:00:00Z"
        )
        return story

    @pytest.fixture
    def api_client(self) -> APIClient:
        """Create an API client for making requests."""
        return APIClient()

    def test_like_story(self, 
                        api_client: APIClient, 
                        user: get_user_model(), 
                        story: Story) -> None:
        """Test liking a story."""
        api_client.force_authenticate(user=user)
        url = reverse("toggle-story-like", kwargs={"story_id": story.id})
        response = api_client.post(url)

        assert response.status_code == status.HTTP_201_CREATED
        assert "Story liked." in response.data["detail"]
        assert StoryLike.objects.filter(user=user, story=story).exists()

    def test_unlike_story(self, 
                          api_client: APIClient, 
                          user: get_user_model(), 
                          story: Story) -> None:
        """Test unliking a story."""

        StoryLike.objects.create(user=user, story=story)
        api_client.force_authenticate(user=user)
        url = reverse("toggle-story-like", kwargs={"story_id": story.id})
        
        response = api_client.post(url)
        assert response.status_code == status.HTTP_200_OK
        assert "Story unliked." in response.data["detail"]
        assert not StoryLike.objects.filter(user=user, story=story).exists()

    def test_story_not_found(self, api_client: APIClient, user: get_user_model()) -> None:
        """Test case when the story does not exist."""
        api_client.force_authenticate(user=user)
        non_existing_story_id = 999999
        url = reverse("toggle-story-like", kwargs={"story_id": non_existing_story_id})

        response = api_client.post(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "No Story matches the given query." in response.data["detail"]

    def test_toggle_like_with_database_error(self, 
                                             api_client: APIClient, 
                                             user: get_user_model(), 
                                             story: Story, 
                                             mocker: mock.MagicMock) -> None:
        """Test case where a database error occurs during like/unlike."""

        mocker.patch("likes.models.StoryLike.toggle_like", side_effect=IntegrityError)
        api_client.force_authenticate(user=user)
        url = reverse("toggle-story-like", kwargs={"story_id": story.id})

        response = api_client.post(url)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "Database error occurred." in response.data["detail"]

    def test_toggle_like_with_unexpected_error(self, 
                                               api_client: APIClient, 
                                               user: get_user_model(), 
                                               story: Story, 
                                               mocker: mock.MagicMock) -> None:
        """Test case where an unexpected error occurs."""
  
        mocker.patch(
            "likes.models.StoryLike.toggle_like", 
            side_effect=Exception("Unexpected error")
        )

        api_client.force_authenticate(user=user)
        url = reverse("toggle-story-like", kwargs={"story_id": story.id})

        response = api_client.post(url)
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "An unexpected error occurred." in response.data["detail"]
