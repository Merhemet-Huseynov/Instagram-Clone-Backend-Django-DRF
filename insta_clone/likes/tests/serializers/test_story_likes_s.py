import pytest
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.utils import timezone
from stories.models import Story
from likes.models import StoryLike
from likes.serializers import StoryLikeSerializer


@pytest.fixture
def user() -> get_user_model():
    """
    Creates a test user.

    Returns:
        CustomUser: A test user instance.
    """
    return get_user_model().objects.create_user(
        email="testuser@example.com", 
        password="password123"
    )

@pytest.fixture
def story(user: get_user_model()) -> Story:
    """
    Creates a test story.

    Args:
        user (CustomUser): The user who owns the story.

    Returns:
        Story: A test story instance.
    """
    return Story.objects.create(
        user=user,
        created_at=timezone.make_aware(timezone.datetime(2025, 3, 15, 0, 0, 0)),
        expires_at=timezone.make_aware(timezone.datetime(2025, 3, 16, 0, 0, 0)),
    )

@pytest.fixture
def story_like(user: get_user_model(), story: Story) -> StoryLike:
    """
    Creates a test story like.

    Args:
        user (CustomUser): The user who liked the story.
        story (Story): The story that is liked.

    Returns:
        StoryLike: A test story like instance.
    """
    return StoryLike.objects.create(user=user, story=story)

@pytest.mark.django_db
def test_story_like_serializer(story_like: StoryLike) -> None:
    """
    Tests whether StoryLikeSerializer correctly serializes a StoryLike instance.

    Args:
        story_like (StoryLike): The story like instance to be serialized.

    Raises:
        AssertionError: If the serialized data does not match the expected values.
    """
    serializer = StoryLikeSerializer(story_like)

    local_created_at = timezone.localtime(
        story_like.created_at).strftime("%Y-%m-%d %H:%M:%S")

    assert serializer.data["user"] == story_like.user.id
    assert serializer.data["story"] == story_like.story.id
    assert serializer.data["created_at"] == local_created_at 
