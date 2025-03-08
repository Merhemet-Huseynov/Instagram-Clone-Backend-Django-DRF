import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.db.models import Model
from rest_framework.response import Response

User = get_user_model()


@pytest.fixture
def create_user(db) -> Model:
    """Creates a user for testing.

    Returns:
        Model: The created user object.
    """
    return User.objects.create_user(
        email="test@example.com", 
        password="testpassword"
    )

@pytest.fixture
def api_client() -> APIClient:
    """Returns an API test client.

    Returns:
        APIClient: The test client.
    """
    return APIClient()

@pytest.mark.django_db
def test_login_success(api_client: APIClient, create_user: Model) -> None:
    """Tests successful login with correct email and password.

    Args:
        api_client (APIClient): The test client.
        create_user (Model): The created user for testing.
    """
    data = {"email": "test@example.com", "password": "testpassword"}
    response: Response = api_client.post("/api/v1/users/login/", data)

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data

@pytest.mark.django_db
def test_login_invalid_credentials(api_client: APIClient) -> None:
    """Tests failed login with invalid email or password.

    Args:
        api_client (APIClient): The test client.
    """
    data = {"email": "wrong@example.com", "password": "wrongpassword"}
    response: Response = api_client.post("/api/v1/users/login/", data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "non_field_errors" in response.data

@pytest.mark.django_db
def test_login_missing_fields(api_client: APIClient) -> None:
    """Tests failed login with missing email or password.

    Args:
        api_client (APIClient): The test client.
    """
    data = {"email": "", "password": ""}
    response: Response = api_client.post("/api/v1/users/login/", data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data
    assert "password" in response.data
