import pytest
from django.contrib.auth import get_user_model
from django.db import models
from posts.models import Post
from likes.models import PostLike
from typing import Type

User = get_user_model()  

@pytest.mark.django_db
class TestPostLikeModel:
    """
    Tests for the PostLike model.
    """

    @pytest.fixture
    def user(self) -> Type[User]:  
        """Fixture to create a user."""
        return User.objects.create_user(
            email="user@example.com",
            password="password123",
        )

    @pytest.fixture
    def post(self, user) -> Post:
        """Fixture to create a post."""
        return Post.objects.create(
            user=user,
            image="image.jpg",
        )

    @pytest.fixture
    def post_like(self, user, post) -> PostLike:
        """Fixture to create a post like."""
        return PostLike.objects.create(user=user, post=post)

    def test_create_like(self, post_like):
        """Test that a user can like a post."""
        assert post_like.user is not None
        assert post_like.post is not None
        assert PostLike.objects.count() == 1

    def test_toggle_like_adds_like(self, user, post):
        """Test toggling like on a post adds a like."""
        was_liked = PostLike.toggle_like(user, post)
        assert was_liked is True
        assert PostLike.objects.filter(user=user, post=post).exists()

    def test_toggle_like_removes_like(self, user, post):
        """Test toggling like on a post removes a like if it already exists."""
        PostLike.objects.create(user=user, post=post)
        was_liked = PostLike.toggle_like(user, post)
        assert was_liked is False
        assert not PostLike.objects.filter(user=user, post=post).exists()
