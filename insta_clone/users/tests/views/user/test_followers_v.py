import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from users.models import CustomUser, Follow


@pytest.fixture
def api_client() -> APIClient:
    """
    Provides a new instance of APIClient for making requests.
    """
    return APIClient()

@pytest.fixture
def user1(db) -> CustomUser:
    """
    Creates and returns a user instance for user1.
    """
    return CustomUser.objects.create_user(email="user1@example.com", password="password123")

@pytest.fixture
def user2(db) -> CustomUser:
    """
    Creates and returns a user instance for user2.
    """
    return CustomUser.objects.create_user(email="user2@example.com", password="password123")

@pytest.mark.django_db
def test_follow_user(api_client: APIClient, user1: CustomUser, user2: CustomUser) -> None:
    """
    Test following another user.
    
    Verifies that a user can successfully follow another user, 
    and the follow relationship is created in the database.
    """
    api_client.force_authenticate(user=user1)
    url = reverse("follow-toggle", kwargs={"username": user2.slug})
    response = api_client.post(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data["message"] == "Followed successfully"
    assert Follow.objects.filter(follower=user1, followed=user2).exists()

@pytest.mark.django_db
def test_unfollow_user(api_client: APIClient, user1: CustomUser, user2: CustomUser) -> None:
    """
    Test unfollowing a user.
    
    Verifies that a user can successfully unfollow another user, 
    and the follow relationship is removed from the database.
    """
    Follow.objects.create(follower=user1, followed=user2)
    api_client.force_authenticate(user=user1)
    url = reverse("follow-toggle", kwargs={"username": user2.slug})
    response = api_client.post(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data["message"] == "Unfollowed successfully"
    assert not Follow.objects.filter(follower=user1, followed=user2).exists()

@pytest.mark.django_db
def test_cannot_follow_self(api_client: APIClient, user1: CustomUser) -> None:
    """
    Test that a user cannot follow themselves.
    
    Verifies that an error is returned when a user tries to follow their own account.
    """
    api_client.force_authenticate(user=user1)
    url = reverse("follow-toggle", kwargs={"username": user1.slug})
    response = api_client.post(url)
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["error"] == "You cannot follow yourself"

@pytest.mark.django_db
def test_follow_non_existent_user(api_client: APIClient, user1: CustomUser) -> None:
    """
    Test following a non-existent user.
    
    Verifies that an error is returned when a user tries to follow a non-existent user.
    """
    api_client.force_authenticate(user=user1)
    url = reverse("follow-toggle", kwargs={"username": "nonexistent-user"})
    response = api_client.post(url)
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data["error"] == "User not found"
