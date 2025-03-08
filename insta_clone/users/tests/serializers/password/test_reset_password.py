import pytest
from django.contrib.auth import get_user_model
from users.models import VerificationCode
from rest_framework.exceptions import ValidationError
from users.serializers import ResetPasswordSerializer

User = get_user_model()


@pytest.fixture
def user() -> User:
    """
    Creates a test user.
    """
    return User.objects.create_user(
        email="testuser@example.com", 
        password="oldpassword"
    )

@pytest.fixture
def verification_code(user: User) -> VerificationCode:
    """
    Creates a verification code for the test user.
    """
    return VerificationCode.objects.create(
        email=user.email,
        verification_code="123456",
        is_verified=False
    )

@pytest.mark.django_db
def test_reset_password_serializer_valid(user: User, verification_code: VerificationCode) -> None:
    """
    Tests that the serializer is valid with correct 
    email, verification code, and new password.
    """
    data = {
        "email": user.email,
        "verification_code": "123456",
        "new_password": "newpassword123"
    }
    
    serializer = ResetPasswordSerializer(data=data)
    assert serializer.is_valid()
    user = serializer.save()
    assert user.check_password("newpassword123")
    verification_code.refresh_from_db()
    assert verification_code.is_verified

@pytest.mark.django_db
def test_reset_password_serializer_invalid_email() -> None:
    """
    Tests that the serializer raises an error for a non-existent email.
    """
    data = {
        "email": "invalid@example.com",
        "verification_code": "123456",
        "new_password": "newpassword123"
    }

    serializer = ResetPasswordSerializer(data=data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)

@pytest.mark.django_db
def test_reset_password_serializer_invalid_verification_code(user: User) -> None:
    """
    Tests that the serializer raises an error for an incorrect verification code.
    """
    data = {
        "email": user.email,
        "verification_code": "654321",
        "new_password": "newpassword123"
    }

    serializer = ResetPasswordSerializer(data=data)
    with pytest.raises(ValidationError):
        serializer.is_valid(raise_exception=True)
