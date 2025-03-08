import pytest
from django.utils import timezone
from datetime import timedelta
from users.models import VerificationCode


@pytest.mark.django_db
def test_verification_code_creation():
    """Test creating a verification code and ensuring it's saved correctly."""
    verification_code = VerificationCode.objects.create(
        email="test@example.com",
        verification_code="123456"
    )
    # Ensure the verification code is created and saved in the database
    assert verification_code.email == "test@example.com"
    assert verification_code.verification_code == "123456"
    assert verification_code.is_verified is False  # Default is False
    assert verification_code.created_at is not None


@pytest.mark.django_db
def test_verification_code_expired():
    """Test that the verification code expires after 3 minutes."""
    verification_code = VerificationCode.objects.create(
        email="test@example.com",
        verification_code="123456"
    )
    
    # Simulate the passage of time beyond 3 minutes
    verification_code.created_at = timezone.now() - timedelta(minutes=4)
    verification_code.save()
    
    # Assert that the code has expired
    assert verification_code.is_expired() is True


@pytest.mark.django_db
def test_verification_code_not_expired():
    """Test that the verification code is not expired within 3 minutes."""
    verification_code = VerificationCode.objects.create(
        email="test@example.com",
        verification_code="123456"
    )
    
    # Simulate the passage of time within 3 minutes
    verification_code.created_at = timezone.now() - timedelta(minutes=2)
    verification_code.save()
    
    # Assert that the code has not expired
    assert verification_code.is_expired() is False


@pytest.mark.django_db
def test_verification_code_verified():
    """Test the scenario where the verification code is marked as verified."""
    verification_code = VerificationCode.objects.create(
        email="test@example.com",
        verification_code="123456"
    )
    
    # Mark the code as verified
    verification_code.is_verified = True
    verification_code.save()
    
    # Assert that the code is marked as verified
    assert verification_code.is_verified is True
