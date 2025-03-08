import pytest
from users.models import CustomUser 
from rest_framework.test import APIClient
from users.models import VerificationCode
from unittest.mock import patch, MagicMock

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client() -> APIClient:
    """
    Fixture to initialize an APIClient instance for testing.

    Returns:
        APIClient: The instance of the APIClient.
    """
    return APIClient()


@pytest.fixture
def test_user() -> CustomUser:
    """
    Fixture to create a test user for authentication tests.

    Returns:
        CustomUser: The test user instance.
    """
    return CustomUser.objects.create_user(
        email="test@example.com",
        password="testpassword"
    )


@pytest.mark.django_db
def test_reset_password_send_code_success(api_client: APIClient, test_user: CustomUser) -> None:
    """
    Test for successfully sending a reset password verification code.

    Args:
        api_client (APIClient): The APIClient instance for making requests.
        test_user (CustomUser): The test user to trigger the password reset for.

    Asserts:
        - A 200 status code is returned.
        - The response contains the correct email and message.
        - A verification code is created in the database.
        - The email sending function is called once with the correct email.
    """
    with patch("services.auth.verification_service.send_verification_email.delay") as mock_send_email:
        response = api_client.post(
            "/api/v1/users/reset-password-send-code/", 
            {
                "email": "test@example.com" 
            }
        )

        assert response.status_code == 200
        assert response.data["email"] == "test@example.com"
        assert response.data["message"] == "Verification code sent."
        assert VerificationCode.objects.filter(email="test@example.com").exists()

        mock_send_email.assert_called_once_with("test@example.com")


@pytest.mark.django_db
def test_reset_password_send_code_invalid_user(api_client: APIClient) -> None:
    """
    Test for sending a reset password verification code to a non-existing user.

    Args:
        api_client (APIClient): The APIClient instance for making requests.

    Asserts:
        - A 400 status code is returned.
        - The error message indicates that the user does not exist.
    """
    response = api_client.post(
        "/api/v1/users/reset-password-send-code/", 
        {
            "email": "nonexistent@example.com" 
        }
    )

    assert response.status_code == 400
    assert "User with this email does not exist." in response.data["email"]


@pytest.mark.django_db
def test_reset_password_send_code_invalid_request(api_client: APIClient) -> None:
    """
    Test for sending a reset password verification code with an invalid request (missing email).

    Args:
        api_client (APIClient): The APIClient instance for making requests.

    Asserts:
        - A 400 status code is returned.
        - The response contains a missing "email" field.
    """
    response = api_client.post(
        "/api/v1/users/reset-password-send-code/", 
        {}
    )

    assert response.status_code == 400
    assert "email" in response.data
