from django.urls import reverse 
from rest_framework import status  
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from posts.models import Post
from comments.models import Comment
from typing import Callable


@pytest.fixture
def user() -> get_user_model():
    """
    Fixture to create a user for authentication in tests.

    Returns:
        User object
    """
    user = get_user_model().objects.create_user(
        email="testuser@example.com", 
        password="password"
    )
    return user

@pytest.fixture
def authenticated_client(user: get_user_model) -> APIClient:
    """
    Fixture to create an authenticated API client for making requests.

    Args:
        user: A user object to authenticate the client.

    Returns:
        APIClient object with authentication
    """
    client = APIClient()
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def post(user: get_user_model) -> Post:
    """
    Fixture to create a post object for testing comment functionality.

    Args:
        user: A user object who will own the post.

    Returns:
        Post object
    """
    post = Post.objects.create(
        user=user,
        image="path/to/image.jpg", 
        caption="Test caption"
    )
    return post

@pytest.fixture
def comment_factory() -> Callable[[Post, get_user_model, str], Comment]:
    """
    Fixture that creates comments for a post.

    Returns:
        A callable that creates a comment for a post with a given user.
    """
    def create_comment(post: Post, user: get_user_model, text: str = "Test comment") -> Comment:
        return Comment.objects.create(
            post=post, 
            user=user, 
            text=text
        )
    return create_comment

@pytest.mark.django_db
def test_create_comment(
                    authenticated_client: APIClient,
                    user: get_user_model, post: Post, 
                    comment_factory: Callable) -> None:
    """
    Test case for creating a comment on a post.

    Args:
        authenticated_client: Authenticated API client to send requests.
        user: The user who creates the comment.
        post: The post on which the comment is being created.
        comment_factory: Factory function to create a comment.

    Asserts:
        The comment is created successfully and exists in the database.
    """
    url = reverse("create_comment", kwargs={"post_id": post.id})
    data = {"text": "Test comment"}
    
    response = authenticated_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert Comment.objects.filter(post=post, user=user, text="Test comment").exists()

@pytest.mark.django_db
def test_create_comment_invalid_data(authenticated_client: APIClient, post: Post) -> None:
    """
    Test case for creating a comment with invalid data (empty text).

    Args:
        authenticated_client: Authenticated API client to send requests.
        post: The post on which the comment is being created.

    Asserts:
        The request returns a 400 BAD REQUEST status and validation error.
    """
    url = reverse("create_comment", kwargs={"post_id": post.id})
    data = {"text": ""} 
    
    response = authenticated_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "This field may not be blank." in response.data["text"]

@pytest.mark.django_db
def test_create_comment_unauthenticated(client: APIClient, post: Post) -> None:
    """
    Test case for creating a comment without authentication.

    Args:
        client: Unauthenticated API client to send requests.
        post: The post on which the comment is being created.

    Asserts:
        The request returns a 401 UNAUTHORIZED status.
    """
    url = reverse("create_comment", kwargs={"post_id": post.id})
    data = {"text": "Test comment"}
    
    response = client.post(url, data)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_list_comments_no_comments(authenticated_client: APIClient, post: Post) -> None:
    """
    Test case for listing comments when no comments exist.

    Args:
        authenticated_client: Authenticated API client to send requests.
        post: The post to list comments for.

    Asserts:
        The request returns a 200 OK status and an empty list of comments.
    """
    url = reverse("list_comments", kwargs={"post_id": post.id})
    
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == []

@pytest.mark.django_db
def test_list_comments_unauthenticated(client: APIClient, post: Post) -> None:
    """
    Test case for listing comments without authentication.

    Args:
        client: Unauthenticated API client to send requests.
        post: The post to list comments for.

    Asserts:
        The request returns a 401 UNAUTHORIZED status.
    """
    url = reverse("list_comments", kwargs={"post_id": post.id})
    
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
