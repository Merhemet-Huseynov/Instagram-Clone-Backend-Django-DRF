import pytest
from pytest import approx
from django.utils import timezone
from datetime import timedelta

from stories.models import Story
from likes.models import StoryLike
from users.models import CustomUser


@pytest.mark.django_db
def test_story_creation() -> None:
    """
    Tests the correct creation of a Story object.
    
    Verifies that a Story is properly created with the correct user and that
    the "created_at" and "expires_at" fields are set.
    """
    user = CustomUser.objects.create_user(
        email="test@example.com", 
        password="password123"
    )
    story = Story.objects.create(user=user)

    assert story.user == user
    assert story.created_at is not None
    assert story.expires_at is not None

@pytest.mark.django_db
def test_story_expiration() -> None:
    """
    Tests the expiration behavior of a Story object.
    
    Verifies that the "is_expired" method correctly detects whether the story
    has expired based on its "expires_at" field.
    """
    user = CustomUser.objects.create_user(
        email="test@example.com", 
        password="password123"
    )
    past_story = Story.objects.create(
        user=user, 
        expires_at=timezone.now() - timedelta(hours=1)
    )
    assert past_story.is_expired is True
    
    future_story = Story.objects.create(
        user=user, 
        expires_at=timezone.now() + timedelta(hours=1)
    )
    assert future_story.is_expired is False 

@pytest.mark.django_db
def test_get_like_count() -> None:
    """
    Tests the get_like_count method of the Story model.
    
    Verifies that the "get_like_count" method correctly counts the number of likes
    a story has received, both initially and after adding/removing likes.
    """
    user1 = CustomUser.objects.create_user(
        email="user1@example.com", 
        password="password123"
    )
    user2 = CustomUser.objects.create_user(
        email="user2@example.com", 
        password="password123"
    )
    
    story = Story.objects.create(user=user1)
    assert story.get_like_count() == 0

    StoryLike.objects.create(user=user1, story=story)
    StoryLike.objects.create(user=user2, story=story)
    assert story.get_like_count() == 2 

    StoryLike.objects.filter(
        user=user1, 
        story=story
    ).delete()
    assert story.get_like_count() == 1
