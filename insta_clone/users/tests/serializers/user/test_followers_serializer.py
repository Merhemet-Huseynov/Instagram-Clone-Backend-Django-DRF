import pytest
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ValidationError as DRFValidationError
from users.models.followers import Follow
from users.serializers.user import FollowSerializer
from django.contrib.auth import get_user_model


@pytest.fixture
def user() -> "User":
    """
    Fixture to create a test user.

    Returns:
        User: A user instance for testing purposes.
    """
    return get_user_model().objects.create_user(
        email="testuser@example.com", password="password123"
    )


@pytest.fixture
def followed_user() -> "User":
    """
    Fixture to create a followed user.

    Returns:
        User: A user instance that will be followed.
    """
    return get_user_model().objects.create_user(
        email="followeduser@example.com", 
        password="password123"
    )


@pytest.fixture
def follow(user: "User", followed_user: "User") -> Follow:
    """
    Fixture to create a Follow instance between two users.

    Args:
        user (User): The follower user.
        followed_user (User): The user being followed.

    Returns:
        Follow: A Follow instance between the two users.
    """
    return Follow.objects.create(follower=user, followed=followed_user)


@pytest.mark.django_db
def test_follow_serializer_valid(follow: Follow) -> None:
    """
    Test the valid serialization of a Follow instance.

    Args:
        follow (Follow): The Follow instance to be serialized.

    Asserts:
        - The serializer should be valid.
        - The serialized data should contain the correct keys and values.
    """
    serializer = FollowSerializer(instance=follow)
    serialized_data = serializer.data

    assert set(serialized_data.keys()) == {"follower", "followed", "created_at"}
    assert serialized_data["follower"] == follow.follower.id
    assert serialized_data["followed"] == follow.followed.id


@pytest.mark.django_db
def test_follow_serializer_invalid_missing_required_fields() -> None:
    """
    Test the Follow serializer when required fields are missing.

    Ensures that the serializer raises a validation error when 
    the required fields are not provided.

    Asserts:
        - The serializer should raise a ValidationError.
    """
    data = {
        "followed": 1,
    }
    serializer = FollowSerializer(data=data)
    with pytest.raises(DRFValidationError):
        serializer.is_valid(raise_exception=True)