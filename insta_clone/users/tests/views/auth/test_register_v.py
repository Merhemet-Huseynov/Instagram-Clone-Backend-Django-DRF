import pytest
from rest_framework import status
from django.urls import reverse
from users.models import CustomUser, VerificationCode
from rest_framework.test import APIClient
from typing import Callable


@pytest.fixture
def create_verification_code() -> Callable[[str], str]:
    """
    Fixture to create a valid verification code for testing.
    
    Args:
        email (str): The email address to associate the verification code with.
        
    Returns:
        str: The verification code generated for the email.
    """
    def _create_code(email: str) -> str:
        verification_code = "123456"
        VerificationCode.objects.create(
            email=email, 
            verification_code=verification_code
        )
        return verification_code
    return _create_code

@pytest.fixture
def client() -> APIClient:
    """
    Fixture to create an APIClient instance for testing.
    
    Returns:
        APIClient: An instance of the APIClient for making requests.
    """
    return APIClient()

@pytest.mark.django_db
def test_register_user_success(
                client: APIClient, 
                create_verification_code: Callable[[str], str]) -> None:
    """
    Test successful registration with valid data.
    
    Args:
        client (APIClient): The client instance to make requests.
        create_verification_code (Callable): Fixture to create a verification code.
        
    Returns:
        None
    """
    email = "testuser@example.com"
    password = "testpassword123"
    first_name = "Test"
    last_name = "User"
    verification_code = create_verification_code(email)

    data = {
        "email": email,
        "verification_code": verification_code,
        "first_name": first_name,
        "last_name": last_name,
        "password": password,
    }

    url = reverse("register")
    response = client.post(url, data, format="multipart")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["message"] == "Registration successful."
    assert CustomUser.objects.filter(email=email).exists()
    assert VerificationCode.objects.filter(email=email, is_verified=True).exists()

@pytest.mark.django_db
def test_register_user_email_already_exists(
                client: APIClient, 
                create_verification_code: Callable[[str], str]) -> None:
    """
    Test that registration fails if email is already registered.
    
    Args:
        client (APIClient): The client instance to make requests.
        create_verification_code (Callable): Fixture to create a verification code.
        
    Returns:
        None
    """
    email = "testuser@example.com"
    password = "testpassword123"
    first_name = "Test"
    last_name = "User"
    verification_code = create_verification_code(email)

    CustomUser.objects.create_user( 
        email=email, 
        password=password, 
        first_name=first_name, 
        last_name=last_name
    )

    data = {
        "email": email,
        "verification_code": verification_code,
        "first_name": first_name,
        "last_name": last_name,
        "password": password,
    }

    url = reverse("register")

    response = client.post(url, data, format="multipart")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data
    assert response.data["email"] == ["This email is already registered."]

@pytest.mark.django_db
def test_register_user_invalid_verification_code(client: APIClient) -> None:
    """
    Test that registration fails if the verification code is incorrect.
    
    Args:
        client (APIClient): The client instance to make requests.
        
    Returns:
        None
    """
    email = "testuser@example.com"
    password = "testpassword123"
    first_name = "Test"
    last_name = "User"
    incorrect_verification_code = "654321"

    data = {
        "email": email,
        "verification_code": incorrect_verification_code,
        "first_name": first_name,
        "last_name": last_name,
        "password": password,
    }

    url = reverse("register")

    response = client.post(url, data, format="multipart")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "verification_code" in response.data
    assert response.data["verification_code"] == ["Invalid or expired verification code."]

@pytest.mark.django_db
def test_register_user_missing_verification_code(client: APIClient) -> None:
    """
    Test that registration fails if the verification code is missing.
    
    Args:
        client (APIClient): The client instance to make requests.
        
    Returns:
        None
    """
    email = "testuser@example.com"
    password = "testpassword123"
    first_name = "Test"
    last_name = "User"

    data = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "password": password,
    }

    url = reverse("register")
    response = client.post(url, data, format="multipart")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "verification_code" in response.data
    assert response.data["verification_code"] == ["This field is required."]