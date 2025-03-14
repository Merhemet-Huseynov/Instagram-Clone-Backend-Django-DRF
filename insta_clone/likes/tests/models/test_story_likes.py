import pytest
from django.contrib.auth import get_user_model
from stories.models import Story
from likes.models import StoryLike
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


@pytest.mark.django_db
def test_toggle_like() -> None:
    """Test toggling like functionality for a story."""
    user: User = User.objects.create_user(
        email="test@example.com", 
        password="testpass"
    )
    story: Story = Story.objects.create(
        user=user, 
        expires_at=timezone.now() + timedelta(hours=24)
    )
    
    # First like should return True and create a like record
    assert StoryLike.toggle_like(user, story) is True
    assert StoryLike.objects.filter(user=user, story=story).exists() is True
    
    # Second like should unlike the story and return False
    assert StoryLike.toggle_like(user, story) is False
    assert StoryLike.objects.filter(user=user, story=story).exists() is False

@pytest.mark.django_db
def test_multiple_users_liking_story() -> None:
    """Test multiple users liking and unliking a story."""
    user1: User = User.objects.create_user(
        email="user1@example.com", 
        password="testpass"
    )
    user2: User = User.objects.create_user(
        email="user2@example.com", 
        password="testpass"
    )
    story: Story = Story.objects.create(
        user=user1, 
        expires_at=timezone.now() + timedelta(hours=24)
    )
    
    # Both users like the story
    assert StoryLike.toggle_like(user1, story) is True
    assert StoryLike.toggle_like(user2, story) is True
    
    # The story should have 2 likes
    assert story.likes.count() == 2
    
    # One user unlikes the story, reducing the like count
    assert StoryLike.toggle_like(user1, story) is False
    assert story.likes.count() == 1
