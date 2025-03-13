import pytest
from likes.serializers import PostLikeSerializer
from likes.models import PostLike
from posts.models import Post
from django.contrib.auth import get_user_model
from datetime import datetime
from typing import Dict

User = get_user_model()


@pytest.mark.django_db
def test_post_like_serializer() -> None:
    """
    Test case for the PostLikeSerializer.

    Creates a user, post, and like instance, then serializes the like
    instance and checks that the necessary fields are included in the serialized data,
    including a correctly formatted creation date.
    """
    user = User.objects.create_user(
        email="test@example.com", 
        password="password"
    )
    post = Post.objects.create(
        user=user, 
        image="test.jpg", 
        caption="Test caption"
    )
    like = PostLike.objects.create(
        user=user, 
        post=post
    )
    
    serializer = PostLikeSerializer(instance=like)
    data: Dict = serializer.data 
    
    assert "id" in data
    assert "user" in data
    assert "post" in data
    assert "formatted_date" in data
    
    expected_date = like.created_at.strftime("%Y-%m-%d %H:%M:%S")
    assert data["formatted_date"] == expected_date

@pytest.mark.django_db
def test_post_like_serializer_read_only_fields() -> None:
    """
    Test case to check that the PostLikeSerializer's read-only fields are correct.

    Creates a user, post, and like instance, serializes the like instance, and ensures
    that the id, user, and formatted_date fields are present in the serialized data.
    """
    user = User.objects.create_user(
        email="readonly@example.com", 
        password="password"
    )
    post = Post.objects.create(
        user=user, 
        image="readonly.jpg", 
        caption="Readonly caption"
    )
    like = PostLike.objects.create(
        user=user, 
        post=post
    )
    serializer = PostLikeSerializer(
        instance=like
    )
    
    assert "id" in serializer.data
    assert "user" in serializer.data
    assert "formatted_date" in serializer.data
