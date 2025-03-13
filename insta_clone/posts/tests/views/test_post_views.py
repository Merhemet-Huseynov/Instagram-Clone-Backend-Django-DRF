import pytest
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from posts.models import Post
from users.models import Follow
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image
from typing import Generator


@pytest.fixture
def user() -> get_user_model():
    """Create a user for testing."""
    return get_user_model().objects.create_user(
        email="testuser@example.com", 
        password="testpassword"
    )

@pytest.fixture
def other_user() -> get_user_model():
    """Create another user for testing follow functionality."""
    return get_user_model().objects.create_user(
        email="otheruser@example.com", 
        password="otherpassword"
    )

@pytest.fixture
def post(user: get_user_model()) -> Post:
    """Create a post for the user."""
    return Post.objects.create(
        user=user,
        image=SimpleUploadedFile(
            "test_image.jpg", 
            b"file_content",
            content_type="image/jpeg"
        ),
        caption="Test post",
    )

@pytest.fixture
def client() -> APIClient:
    """Create an API client."""
    return APIClient()

def create_image() -> SimpleUploadedFile:
    """Create a simple image file for testing."""
    img = Image.new("RGB", (100, 100), color="red")
    image_file = BytesIO()
    img.save(image_file, "JPEG")
    image_file.seek(0)
    return SimpleUploadedFile(
        "test_image.jpg", 
        image_file.read(), 
        content_type="image/jpeg"
    )

@pytest.mark.django_db
def test_create_post(client: APIClient, user: get_user_model()) -> None:
    """Test creating a new post."""
    client.force_authenticate(user=user)
    image = create_image()
    
    data = {
        "image": image,
        "caption": "Test post caption"
    }
    
    response = client.post(
        "/api/v1/posts/post-create/", 
        data, 
        format="multipart"
    )
    assert response.status_code == status.HTTP_201_CREATED

    post = Post.objects.first()
    assert post is not None
    assert post.caption == "Test post caption"
    assert post.image.name.startswith("posts/")

@pytest.mark.django_db
def test_create_post_unauthorized(client: APIClient) -> None:
    """Test creating a post without authentication.""" 
    image = SimpleUploadedFile(
        "test_image.jpg", 
        b"file_content", 
        content_type="image/jpeg"
    )
    data = {
        "image": image, 
        "caption": "Test post caption"
    }
    response = client.post(
        "/api/v1/posts/post-create/", 
        data, 
        format="multipart"
    )  
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_post_list(
        client: APIClient, user: get_user_model(), 
        other_user: get_user_model()
    ) -> None:

    """Test listing posts from followed users."""      
    client.force_authenticate(user=user)
    Follow.objects.create(follower=user, followed=other_user)

    Post.objects.create(
        user=other_user,
        image=SimpleUploadedFile(
            "test_image.jpg", 
            b"file_content", 
            content_type="image/jpeg"
        ),
        caption="Other user post",
    )

    response = client.get("/api/v1/posts/post-list/")
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_post_detail(
        client: APIClient, user: get_user_model(), post: Post
    ) -> None:
    """Test retrieving post details."""
    client.force_authenticate(user=user)
    response = client.get(f"/api/v1/posts/{post.id}/")    
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_delete_post(
        client: APIClient, user: get_user_model(), post: Post
    ) -> None:
    """Test deleting a post by the owner."""
    client.force_authenticate(user=user)
    response = client.delete(f"/api/v1/posts/{post.id}/delete/")
    assert response.status_code == status.HTTP_204_NO_CONTENT

@pytest.mark.django_db
def test_delete_post_forbidden(
        client: APIClient, other_user: get_user_model(), post: Post
    ) -> None:

    """Test deleting a post that is not owned by the user."""
    client.force_authenticate(user=other_user)
    response = client.delete(f"/api/v1/posts/{post.id}/delete/")
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_post_detail_not_found(client: APIClient) -> None:
    """Test retrieving a post that does not exist."""
    response = client.get("/api/posts/999/")
    assert response.status_code == status.HTTP_404_NOT_FOUND