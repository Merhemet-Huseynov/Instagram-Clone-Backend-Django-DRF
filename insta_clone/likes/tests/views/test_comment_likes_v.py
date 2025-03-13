import pytest
from django.contrib.auth import get_user_model
from comments.models import Comment
from likes.models import CommentLike
from posts.models import Post

@pytest.fixture
def user(db):
    """
    Fixture to create a test user.
    """
    User = get_user_model()
    return User.objects.create_user(
        email="testuser@example.com",
        password="testpassword"
    )

@pytest.fixture
def post(user):
    """
    Fixture to create a test post for a given user.
    """
    return Post.objects.create(
        user=user,
        caption="Test caption"
    )

@pytest.fixture
def comment(user, post):
    """
    Fixture to create a test comment.
    """
    return Comment.objects.create(
        text="This is a test comment",
        user=user,
        post=post
    )

@pytest.mark.django_db
def test_toggle_like_creates_like(user, comment):
    """
    Test that liking a comment creates a like.
    """
    assert CommentLike.objects.count() == 0
    
    result = CommentLike.toggle_like(user, comment)
    
    assert result is True
    assert CommentLike.objects.count() == 1
    like = CommentLike.objects.first()
    assert like.user == user
    assert like.comment == comment

@pytest.mark.django_db
def test_toggle_like_removes_like(user, comment):
    """
    Test that unliking a comment removes the like.
    """
    CommentLike.objects.create(user=user, comment=comment)
    assert CommentLike.objects.count() == 1
    
    result = CommentLike.toggle_like(user, comment)
    
    assert result is False
    assert CommentLike.objects.count() == 0

@pytest.mark.django_db
def test_toggle_like_multiple_times(user, comment):
    """
    Test toggling likes multiple times.
    """
    assert CommentLike.objects.count() == 0
    
    assert CommentLike.toggle_like(user, comment) is True
    assert CommentLike.objects.count() == 1
    
    assert CommentLike.toggle_like(user, comment) is False
    assert CommentLike.objects.count() == 0
    
    assert CommentLike.toggle_like(user, comment) is True
    assert CommentLike.objects.count() == 1

@pytest.mark.django_db
def test_toggle_like_nonexistent_comment(user):
    """
    Test that liking a nonexistent comment does not create a like.
    """
    non_existent_comment = Comment.objects.filter(id=-1).first()
    result = CommentLike.toggle_like(user, non_existent_comment)
    assert result is False
    assert CommentLike.objects.count() == 0
