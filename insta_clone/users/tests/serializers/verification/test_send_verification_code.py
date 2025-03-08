import pytest
from rest_framework.test import APIClient
from rest_framework.exceptions import ValidationError

from users.serializers.verification import SendVerificationCodeSerializer
from users.models import VerificationCode
from services.auth import create_verification_code


def send_verification_code(email: str) -> dict:
    """
    Helper function to send a verification code request.

    Args:
        email (str): The email address to send the verification code to.
    
    Returns:
        dict: The response data from the API call.
    """
    client = APIClient()
    response = client.post(
        "/api/v1/users/send-verification-code/", 
        {
            "email": email
        }, 
        format="json"
    )
    return response


@pytest.mark.django_db
def test_send_verification_code_serializer_valid_email() -> None:
    """
    Test that a verification code is successfully sent for a valid email.
    """
    email = "testuser@example.com"
    response = send_verification_code(email)
    
    assert response.status_code == 200
    assert response.data["message"] == "Verification code sent."


@pytest.mark.django_db
def test_send_verification_code_serializer_invalid_email() -> None:
    """
    Test that an invalid email format returns a validation error.
    """
    invalid_email = "invalid-email"
    response = send_verification_code(invalid_email)
    
    assert response.status_code == 400
    assert "email" in response.data


@pytest.mark.django_db
def test_send_verification_code_serializer_existing_verification_code() -> None:
    """
    Test that requesting a verification code for an email that already has an
    existing (non-expired) verification code still allows sending a new code.
    """
    email = "existinguser@example.com"
    create_verification_code(email)
    response = send_verification_code(email)
    
    assert response.status_code == 200
    assert response.data["message"] == "Verification code sent."