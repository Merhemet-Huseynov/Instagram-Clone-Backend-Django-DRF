import pytest
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from users.models import Follow 

User = get_user_model()


@pytest.mark.django_db
def test_follow_creation() -> None:
    """
    Test that a Follow instance can be created with valid follower and followed users.

    Asserts that the created follow instance links the correct users.
    """
    user1 = User.objects.create_user(email="user1@example.com", password="testpass")
    user2 = User.objects.create_user(email="user2@example.com", password="testpass")

    follow = Follow.objects.create(follower=user1, followed=user2)

    assert follow.follower == user1
    assert follow.followed == user2


@pytest.mark.django_db
def test_unique_follow_constraint() -> None:
    """
    Test the unique constraint on the Follow model to prevent duplicate follow entries.

    Asserts that an IntegrityError is raised when attempting to create duplicate follow entries.
    """
    user1 = User.objects.create_user(email="user1@example.com", password="testpass")
    user2 = User.objects.create_user(email="user2@example.com", password="testpass")

    Follow.objects.create(follower=user1, followed=user2)

    with pytest.raises(IntegrityError):
        Follow.objects.create(follower=user1, followed=user2)


@pytest.mark.django_db
def test_self_follow_validation() -> None:
    """
    Test that a user cannot follow themselves.

    Asserts that a ValidationError is raised when trying to create a self-follow instance.
    """
    user = User.objects.create_user(email="user@example.com", password="testpass")

    follow = Follow(follower=user, followed=user)
    
    with pytest.raises(ValidationError):
        follow.full_clean()


@pytest.mark.django_db
def test_toggle_follow_create() -> None:
    """
    Test the toggle_follow method to create a new follow relationship.

    Asserts that a follow relationship is created when it doesn't already exist.
    """
    user1 = User.objects.create_user(email="user1@example.com", password="testpass")
    user2 = User.objects.create_user(email="user2@example.com", password="testpass")

    assert Follow.toggle_follow(user1, user2) is True
    assert Follow.objects.filter(follower=user1, followed=user2).exists()


@pytest.mark.django_db
def test_toggle_follow_remove() -> None:
    """
    Test the toggle_follow method to remove an existing follow relationship.

    Asserts that a follow relationship is removed when it already exists.
    """
    user1 = User.objects.create_user(email="user1@example.com", password="testpass")
    user2 = User.objects.create_user(email="user2@example.com", password="testpass")

    Follow.objects.create(follower=user1, followed=user2)
    
    assert Follow.toggle_follow(user1, user2) is False
    assert not Follow.objects.filter(follower=user1, followed=user2).exists()
