import pytest
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from posts.models import Post
from posts.validators import validate_image_format, validate_image_size
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_validate_image_format_valid() -> None:
    """Test that validate_image_format accepts valid PNG images."""
    image = SimpleUploadedFile(
        "test.png", 
        b"\x89PNG\r\n\x1a\n\x00\x00\x00", 
        content_type="image/png"
    )
    try:
        validate_image_format(image)
    except ValidationError:
        pytest.fail("validate_image_format raised ValidationError unexpectedly!")

@pytest.mark.django_db
def test_validate_image_format_invalid() -> None:
    """Test that validate_image_format raises ValidationError for invalid file formats."""
    image = SimpleUploadedFile(
        "test.txt", 
        b"Random text data", 
        content_type="text/plain"
    )
    with pytest.raises(ValidationError, match="Only JPG and PNG images are allowed."):
        validate_image_format(image)

@pytest.mark.django_db
def test_validate_image_size_valid() -> None:
    """Test that validate_image_size accepts images within the size limit (<= 5MB)."""
    image_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00" + b"\x00" * (4 * 1024 * 1024)
    image = SimpleUploadedFile(
        "test.png", 
        image_content, 
        content_type="image/png"
    )
    try:
        validate_image_size(image)
    except ValidationError:
        pytest.fail("validate_image_size raised ValidationError unexpectedly!")

@pytest.mark.django_db
def test_validate_image_size_invalid() -> None:
    """Test that validate_image_size raises ValidationError for images exceeding 5MB."""
    image_content = b"\x89PNG\r\n\x1a\n\x00\x00\x00" + b"\x00" * (5 * 1024 * 1024 + 1) 
    image = SimpleUploadedFile(
        "test.png", 
        image_content, 
        content_type="image/png"
    )
    with pytest.raises(ValidationError, match="Image size must not exceed 5MB."):
        validate_image_size(image)

@pytest.mark.django_db
def test_create_post() -> None:
    """Test that a Post object is successfully created with a valid user and image."""
    user = User.objects.create_user(
        email="test@example.com", 
        password="password123"
    )
    image = SimpleUploadedFile(
        "test.png", 
        b"\x89PNG\r\n\x1a\n\x00\x00\x00", 
        content_type="image/png"
    )
    post = Post.objects.create(
        user=user, 
        image=image, 
        caption="Test caption"
    )
    
    assert post.user == user
    assert post.caption == "Test caption"
    assert post.image.name.startswith("posts/")
