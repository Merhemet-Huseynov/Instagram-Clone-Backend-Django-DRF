import pytest
from django.utils import timezone
from datetime import timedelta

from stories.models import Story
from users.models import CustomUser
from stories.serializers import StorySerializer


@pytest.mark.django_db
def test_story_serializer() -> None:
    """
    Test StorySerializer to ensure it correctly serializes Story instances.

    This test creates a new CustomUser and Story instance, then serializes the 
    Story instance using StorySerializer. It verifies that the serialized data 
    contains the expected fields with the correct values.

    Steps:
    1. Create a new user instance.
    2. Create a new Story instance associated with the user.
    3. Serialize the Story instance.
    4. Assert the correct serialized fields are returned, including the user's 
       email, creation date, expiration date, and initial like count.

    Asserts:
        - The serialized data contains the correct user email.
        - The serialized data contains the `created_at`, `expires_at`, 
          `image`, `video`, and `like_count` fields.
        - The like count for a newly created story is 0.
    """
    user = CustomUser.objects.create_user(
        email="test@example.com", 
        password="testpassword"
    )
    story = Story.objects.create(
        user=user,
        created_at=timezone.now(),
        expires_at=timezone.now() + timedelta(hours=24)
    )

    serializer = StorySerializer(instance=story)
    data = serializer.data

    assert data["user"] == user.email  
    assert "created_at" in data
    assert "expires_at" in data
    assert "image" in data
    assert "video" in data
    assert "like_count" in data
    assert data["like_count"] == 0 
