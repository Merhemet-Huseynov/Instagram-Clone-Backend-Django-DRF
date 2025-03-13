import pytest
from django.contrib.auth import get_user_model
from comments.models import Comment
from likes.models import CommentLike
from posts.models import Post
from typing import Type

User = get_user_model()


@pytest.fixture
def user() -> Type[User]:
    """
    Fixture to create a test user.

    Returns:
        User object: The created test user.
    """
    User = get_user_model()
    return User.objects.create_user(
        email="testuser@example.com", 
        password="testpassword"
    )

@pytest.fixture
def post(user: Type[User]) -> Post:
    """
    Fixture to create a test post for a given user.

    Args:
        user (User): The user object to associate with the post.

    Returns:
        Post object: The created test post.
    """
    return Post.objects.create(
        user=user, 
        caption="Test caption"
    )

@pytest.fixture
def comment(user: Type[User], post: Post) -> Comment:
    """
    Fixture to create a test comment for a given post and user.

    Args:
        user (User): The user who created the comment.
        post (Post): The post to which the comment belongs.

    Returns:
        Comment object: The created test comment.
    """
    return Comment.objects.create(
        text="This is a test comment", 
        user=user, 
        post=post
    )

@pytest.mark.django_db
def test_toggle_like_creates_like(user: Type[User], comment: Comment) -> None:
    """
    Test case to check that a like is created when the user likes a comment.

    Args:
        user (User): The user who likes the comment.
        comment (Comment): The comment being liked.
    """
    assert CommentLike.objects.count() == 0

    result = CommentLike.toggle_like(user, comment)
    assert result is True
    assert CommentLike.objects.count() == 1

    like = CommentLike.objects.first()
    assert like.user == user
    assert like.comment == comment

@pytest.mark.django_db
def test_toggle_like_removes_like(user: Type[User], comment: Comment) -> None:
    """
    Test case to check that a like is removed when the user unlikes a comment.

    Args:
        user (User): The user who unlikes the comment.
        comment (Comment): The comment being unliked.
    """
    CommentLike.objects.create(
        user=user, 
        comment=comment
    )
    assert CommentLike.objects.count() == 1
    
    result = CommentLike.toggle_like(user, comment)
    
    assert result is False
    assert CommentLike.objects.count() == 0

@pytest.mark.django_db
def test_toggle_like_multiple_likes(user: Type[User], comment: Comment) -> None:
    """
    Test case to check toggling likes multiple times.

    Args:
        user (User): The user who toggles the like on the comment.
        comment (Comment): The comment to toggle likes on.
    """
    result = CommentLike.toggle_like(user, comment)
    assert result is True
    assert CommentLike.objects.count() == 1
    
    result = CommentLike.toggle_like(user, comment)
    assert result is False
    assert CommentLike.objects.count() == 0
    
    result = CommentLike.toggle_like(user, comment)
    assert result is True
    assert CommentLike.objects.count() == 1
