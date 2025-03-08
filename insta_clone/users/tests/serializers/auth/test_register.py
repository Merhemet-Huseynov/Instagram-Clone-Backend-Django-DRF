import pytest
from datetime import timedelta
from django.contrib.auth import get_user_model
from users.models import VerificationCode
from users.serializers import RegisterSerializer
from django.utils.timezone import now
from rest_framework.exceptions import ValidationError

User = get_user_model()


@pytest.mark.django_db
class TestRegisterSerializer:
    """
    Test cases for the RegisterSerializer.
    Ensures that user registration follows the expected behavior with validation checks.
    """

    def setup_method(self) -> None:
        """
        Setup method to initialize common test data.
        """
        self.email: str = "test@example.com"
        self.valid_code: str = "123456"
        self.invalid_code: str = "654321"
        self.user_data: dict[str, str] = {
            "email": self.email,
            "verification_code": self.valid_code,
            "first_name": "Test",
            "last_name": "User",
            "password": "securepassword123",
            "bio": "This is a test bio",
        }
    
    def test_successful_registration(self) -> None:
        """
        Test successful user registration with a valid verification code.
        """
        VerificationCode.objects.create(
            email=self.email,
            verification_code=self.valid_code
        )
        
        serializer = RegisterSerializer(data=self.user_data)
        assert serializer.is_valid(), serializer.errors
        
        user: User = serializer.save()
        assert user.email == self.email
        assert user.first_name == "Test"
        assert VerificationCode.objects.filter(email=self.email, is_verified=True).exists()

    def test_registration_with_existing_email(self) -> None:
        """
        Test that registration fails if the email is already registered.
        """
        User.objects.create_user(email=self.email, password="testpass")
        VerificationCode.objects.create(
            email=self.email,
            verification_code=self.valid_code
        )

        serializer = RegisterSerializer(data=self.user_data)
        with pytest.raises(ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)
        
        assert "This email is already registered." in str(exc_info.value)

    def test_registration_with_invalid_verification_code(self) -> None:
        """
        Test that registration fails if the verification code is invalid.
        """
        VerificationCode.objects.create(
            email=self.email,
            verification_code=self.invalid_code
        )

        serializer = RegisterSerializer(data=self.user_data)
        with pytest.raises(ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)
        
        assert "Invalid or expired verification code." in str(exc_info.value)

    def test_registration_with_already_verified_code(self) -> None:
        """
        Test that registration fails if the verification code is already used.
        """
        VerificationCode.objects.create(
            email=self.email,
            verification_code=self.valid_code,
            is_verified=True
        )

        serializer = RegisterSerializer(data=self.user_data)
        with pytest.raises(ValidationError) as exc_info:
            serializer.is_valid(raise_exception=True)

        assert "Verification code is invalid or expired." in str(exc_info.value)
