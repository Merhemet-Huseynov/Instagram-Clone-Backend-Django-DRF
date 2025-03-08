import pytest
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from django.urls import reverse

User = get_user_model()

@pytest.fixture
def user():
    """Fixture to create a test user."""
    return User.objects.create_user(
        email="testuser@example.com",
        password="oldpassword123"
    )

@pytest.fixture
def client():
    """Fixture to provide a test API client."""
    return APIClient()

@pytest.mark.django_db
class TestChangePasswordView:
    def test_change_password_success(self, user, client):
        """Test that the password can be successfully changed."""
        url = reverse("change-password") 
        client.force_authenticate(user=user)

        data = {
            "old_password": "oldpassword123",
            "new_password": "newpassword123",
            "confirm_password": "newpassword123"
        }

        response = client.post(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["message"] == "Password changed successfully."
        user.refresh_from_db()
        assert user.check_password("newpassword123")

    def test_change_password_invalid_old_password(self, user, client):
        """Test that an error is raised if the old password is incorrect."""
        url = reverse("change-password")
        client.force_authenticate(user=user)

        data = {
            "old_password": "wrongoldpassword",
            "new_password": "newpassword123",
            "confirm_password": "newpassword123"
        }

        response = client.post(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "old_password" in response.data
        assert response.data["old_password"] == ["The old password is incorrect."]

    def test_change_password_mismatched_new_passwords(self, user, client):
        """Test that an error is raised if the new password and confirmation do not match."""
        url = reverse("change-password")
        client.force_authenticate(user=user)

        data = {
            "old_password": "oldpassword123",
            "new_password": "newpassword123",
            "confirm_password": "differentpassword123"
        }

        response = client.post(url, data)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "new_password" in response.data
        assert response.data["new_password"] == ["The new password and confirm password do not match."]

    def test_unauthenticated_user(self, client):
        """Test that an unauthenticated user cannot change their password."""
        url = reverse("change-password")

        data = {
            "old_password": "oldpassword123",
            "new_password": "newpassword123",
            "confirm_password": "newpassword123"
        }

        response = client.post(url, data)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.data["detail"] == "Authentication credentials were not provided."