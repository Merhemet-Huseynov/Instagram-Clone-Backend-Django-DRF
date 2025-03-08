import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIRequestFactory
from users.serializers import ChangePasswordSerializer  

User = get_user_model()


@pytest.fixture
def user() -> User:
    """
    Creates a test user.
    """
    return User.objects.create_user(
        email="testuser@example.com", 
        password="OldPassword123"
    )


@pytest.fixture
def api_request() -> APIRequestFactory:
    """
    Creates a fake API request for testing.
    """
    return APIRequestFactory().post("/fake-url/")


@pytest.mark.django_db
def test_successful_password_change(user: User, api_request: APIRequestFactory) -> None:
    """
    Tests that the password is successfully changed 
    when the correct old password is provided.
    """
    api_request.user = user  
    data = {
        "old_password": "OldPassword123",
        "new_password": "NewSecurePass456",
        "confirm_password": "NewSecurePass456",
    }
    serializer = ChangePasswordSerializer(
        data=data, 
        context={"request": api_request}
    )
    
    assert serializer.is_valid()
    updated_user = serializer.save()
    assert updated_user.check_password("NewSecurePass456")


@pytest.mark.django_db
def test_invalid_old_password(user: User, api_request: APIRequestFactory) -> None:
    """
    Tests that validation error is raised when an incorrect 
    old password is provided.
    """
    api_request.user = user
    data = {
        "old_password": "WrongOldPassword",
        "new_password": "NewSecurePass456",
        "confirm_password": "NewSecurePass456",
    }
    serializer = ChangePasswordSerializer(
        data=data, 
        context={"request": api_request}
    )
    
    with pytest.raises(ValidationError) as excinfo:
        serializer.is_valid(raise_exception=True)
    
    assert "old_password" in excinfo.value.detail


@pytest.mark.django_db
def test_password_mismatch(user: User, api_request: APIRequestFactory) -> None:
    """
    Tests that validation error is raised when the new password 
    and confirmation password do not match.
    """
    api_request.user = user
    data = {
        "old_password": "OldPassword123",
        "new_password": "NewSecurePass456",
        "confirm_password": "MismatchPass789",
    }
    serializer = ChangePasswordSerializer(
        data=data, 
        context={"request": api_request}
    )
    
    with pytest.raises(ValidationError) as excinfo:
        serializer.is_valid(raise_exception=True)
    
    assert "new_password" in excinfo.value.detail
