import pytest
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.response import Response


@pytest.mark.django_db
def test_logout_view(client: APIClient) -> None:
    """
    Test the logout functionality with a valid refresh token.

    Args:
        client: The test client to send requests.

    Asserts:
        - A successful logout response with status code 200.
        - The response contains the message "Successfully logged out."
        - The token is blacklisted.
    """
    user = get_user_model().objects.create_user(
        email="testuser@example.com",
        password="testpassword"
    )

    refresh = RefreshToken.for_user(user)
    logout_data = {"refresh": str(refresh)}
    response: Response = client.post("/api/v1/users/logout/", logout_data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["detail"] == "Successfully logged out."

    try:
        RefreshToken(str(refresh))
        pytest.fail("Token should be blacklisted.")
    except Exception:
        pass

@pytest.mark.django_db
def test_logout_view_invalid_token(client: APIClient) -> None:
    """
    Test the logout functionality with an invalid refresh token.

    Args:
        client: The test client to send requests.

    Asserts:
        - A failed response with status code 400.
        - The response contains the message "Invalid token."
    """

    logout_data = {"refresh": "invalid_token"}
    response: Response = client.post("/api/v1/users/logout/", logout_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["detail"] == "Invalid token."