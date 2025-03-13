import pytest
from django.contrib.auth import get_user_model
from posts.models import Post
from likes.models import PostLike

User = get_user_model()


@pytest.mark.django_db
def test_toggle_like_creates_like() -> None:
    """
    Test that liking a post creates a like entry.
    
    This test simulates a user liking a post and ensures that a 
    corresponding PostLike entry is created in the database.
    """
    user = User.objects.create_user(
        email="test@example.com", 
        password="password"
    )
    post = Post.objects.create(
        user=user, 
        image="test.jpg"
    )
    
    liked = PostLike.toggle_like(user, post)
    assert liked is True
    assert PostLike.objects.filter(user=user, post=post).exists()

@pytest.mark.django_db
def test_toggle_like_removes_like() -> None:
    """
    Test that unliking a post removes the like entry.
    
    This test ensures that when a user unlikes a post, the corresponding
    PostLike entry is deleted from the database.
    """
    user = User.objects.create_user(
        email="test@example.com", 
        password="password"
    )
    post = Post.objects.create(
        user=user, 
        image="test.jpg"
    )
    PostLike.objects.create(
        user=user, 
        post=post
    )
    
    liked = PostLike.toggle_like(user, post)
    assert liked is False
    assert not PostLike.objects.filter(user=user, post=post).exists()

@pytest.mark.django_db
def test_like_count() -> None:
    """
    Test that the like count method returns the correct number of likes.
    
    This test verifies that the get_like_count method of a post correctly 
    reflects the number of likes for that post.
    """
    user1 = User.objects.create_user(
        email="user1@example.com", 
        password="password"
    )
    user2 = User.objects.create_user(
        email="user2@example.com", 
        password="password"
    )
    post = Post.objects.create(
        user=user1, 
        image="test.jpg"
    )
    
    PostLike.toggle_like(user1, post)
    PostLike.toggle_like(user2, post)
    
    assert post.get_like_count() == 2
    
    PostLike.toggle_like(user1, post)
    assert post.get_like_count() == 1
