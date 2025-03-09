import pytest
from django.urls import reverse
from rest_framework import status
from datetime import timedelta

from users.models.daily_messages import DailyMessage
from users.models.daily_message_limit import DailyMessageLimit


@pytest.mark.django_db
def test_send_verification_code_success(client, mocker) -> None:
    """
    Test successful verification code sending.

    Verifies that the verification code is sent successfully, the correct status code 
    is returned, and a DailyMessage record is created for the given email.
    """
    email = "test@example.com"
    mocker.patch("users.tasks.send_verification_email.delay")
    
    response = client.post(
        reverse("send_verification_code"), 
        {
            "email": email
        }
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Verification code sent."}
    assert DailyMessage.objects.filter(email=email).exists()


@pytest.mark.django_db
def test_send_verification_code_daily_limit_exceeded(client, mocker) -> None:
    """
    Test daily limit exceeded response.

    Verifies that when the daily limit for sending verification codes is exceeded, 
    the server responds with status 429 (Too Many Requests).
    """
    email = "test@example.com"

    limit_obj = DailyMessageLimit.objects.create(
        limit=1, 
        reset_time=timedelta(seconds=86400), 
        expiration_time=timedelta(seconds=120) 
    )

    mocker.patch(
        "users.tasks.send_verification_email.delay", 
        return_value=None
    )
    response = client.post(
        "/api/v1/users/send-verification-code/", 
        {
            "email": email
        }
    )
    assert response.status_code == 200

    response = client.post(
        "/api/v1/users/send-verification-code/", 
        {
            "email": email
        }
    )
    assert response.status_code == 429


@pytest.mark.django_db
def test_send_verification_code_expiration_time_not_passed(client, mocker) -> None:
    """
    Test trying to send another verification code before expiration time passes.

    Verifies that if a verification code has already been sent and the expiration time 
    has not yet passed, the server responds with status 429 (Too Many Requests).
    """
    email = "test@example.com"

    limit_obj = DailyMessageLimit.objects.create(
        limit=5, 
        reset_time=timedelta(seconds=86400), 
        expiration_time=timedelta(seconds=300)
    )

    DailyMessage.objects.create(email=email)
    
    response = client.post(
        reverse("send_verification_code"), 
        {
            "email": email
        }
    )
    
    assert response.status_code == status.HTTP_429_TOO_MANY_REQUESTS
    assert "Please, try again in" in response.json()["error"]


@pytest.mark.django_db
def test_send_verification_code_invalid_email(client) -> None:
    """
    Test sending verification code with invalid email format.

    Verifies that an invalid email format results in a 400 Bad Request response 
    with the correct error message.
    """
    response = client.post(
        reverse("send_verification_code"), 
        {
            "email": "invalid-email"
        }
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.json()