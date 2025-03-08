import pytest
from users.models import CustomUser, VerificationCode
from rest_framework.test import APIClient
from django.utils.timezone import now
from datetime import timedelta


@pytest.fixture
def create_user() -> CustomUser:
    """
    Fixture to create a custom user with email and password.

    Returns:
        CustomUser: The created user instance.
    """
    user = CustomUser.objects.create_user(
        email="test@example.com", 
        password="OldPassword123"
    )
    return user


@pytest.fixture
def create_verification_code(create_user: CustomUser) -> VerificationCode:
    """
    Fixture to create a verification code associated with a user.

    Args:
        create_user (CustomUser): The user instance to associate the verification code with.

    Returns:
        VerificationCode: The created verification code instance.
    """
    verification_code = VerificationCode.objects.create(
        email=create_user.email, 
        verification_code="123456", 
        created_at=now()
    )
    return verification_code


@pytest.mark.django_db
def test_reset_password_success(
                        create_user: CustomUser, 
                        create_verification_code: VerificationCode) -> None:
    """
    Test case for successfully resetting the user's password.

    Args:
        create_user (CustomUser): The user instance to reset the password for.
        create_verification_code (VerificationCode): The associated verification code instance.
    
    Asserts:
        - Status code is 200.
        - The password is updated successfully.
        - The verification code is marked as used.
    """
    client = APIClient()
    data = {
        "email": create_user.email, 
        "verification_code": "123456", 
        "new_password": "NewPassword123"
    }
    response = client.post(
        "/api/v1/users/reset-password/", 
        data, 
        format="json"
    )
    
    assert response.status_code == 200
    assert response.data["message"] == "Password reset successful."
    
    create_user.refresh_from_db()
    assert create_user.check_password("NewPassword123")  

    create_verification_code.refresh_from_db()
    assert create_verification_code.is_verified


@pytest.mark.django_db
def test_reset_password_invalid_code(create_user: CustomUser) -> None:
    """
    Test case for attempting to reset the password with an 
    invalid verification code.

    Args:
        create_user (CustomUser): The user instance to reset the password for.
    
    Asserts:
        - Status code is 400.
        - The response contains the "verification_code" error.
    """
    client = APIClient()
    data = {
        "email": create_user.email, 
        "verification_code": "654321",
        "new_password": "NewPassword123"
    }
    response = client.post(
        "/api/v1/users/reset-password/", 
        data, 
        format="json"
    )

    assert response.status_code == 400
    assert "verification_code" in response.data
