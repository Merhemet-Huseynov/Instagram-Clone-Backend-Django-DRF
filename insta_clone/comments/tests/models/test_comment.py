import pytest
from django.contrib.auth import get_user_model
from posts.models import Post
from comments.models import Comment
from likes.models.comment_likes import CommentLike
from typing import List

@pytest.fixture
def user() -> get_user_model():
    """
    Fixture to create a test user.
    Returns:
        User model instance.
    """
    return get_user_model().objects.create_user(
        email="testuser@example.com",
        password="testpassword123"
    )

@pytest.fixture
def post(user: get_user_model()) -> Post:
    """
    Fixture to create a test post for a given user.
    Args:
        user: The user who created the post.
    Returns:
        Post model instance.
    """
    return Post.objects.create(
        caption="Test Post",  
        user=user
    )

@pytest.fixture
def comment(user: get_user_model(), post: Post) -> Comment:
    """
    Fixture to create a test comment for a given post and user.
    Args:
        user: The user who wrote the comment.
        post: The post that the comment belongs to.
    Returns:
        Comment model instance.
    """
    return Comment.objects.create(
        user=user,
        post=post,
        text="This is a test comment."
    )

@pytest.mark.django_db
def test_comment_str(comment: Comment) -> None:
    """
    Test the string representation of a comment.
    Args:
        comment: The comment instance.
    """
    assert str(comment) == f"{comment.user.email} - {comment.text[:30]}"

@pytest.mark.django_db
def test_comment_get_like_count(comment: Comment, user: get_user_model()) -> None:
    """
    Test getting the like count for a comment.
    Args:
        comment: The comment instance.
        user: The user who likes the comment.
    """
    assert comment.get_like_count() == 0
    CommentLike.objects.create(user=user, comment=comment)
    assert comment.get_like_count() == 1

@pytest.mark.django_db
def test_comment_get_users_who_liked(comment: Comment, user: get_user_model()) -> None:
    """
    Test getting the users who liked a comment.
    Args:
        comment: The comment instance.
        user: The user who liked the comment.
    """
    CommentLike.objects.create(user=user, comment=comment)
    users_who_liked: List[int] = comment.get_users_who_liked()
    assert user.id in users_who_liked

@pytest.mark.django_db
def test_comment_like_toggle(comment: Comment, user: get_user_model()) -> None:
    """
    Test toggling the like status for a comment.
    Args:
        comment: The comment instance.
        user: The user who likes/unlikes the comment.
    """
    assert CommentLike.toggle_like(user=user, comment=comment) is True
    assert CommentLike.objects.filter(user=user, comment=comment).exists()
    assert CommentLike.toggle_like(user=user, comment=comment) is False
    assert not CommentLike.objects.filter(user=user, comment=comment).exists()
