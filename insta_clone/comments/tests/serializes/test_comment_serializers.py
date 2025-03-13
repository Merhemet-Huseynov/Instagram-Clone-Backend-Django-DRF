import pytest
from comments.models import Comment
from users.models import CustomUser
from posts.models import Post
from comments.serializers import CommentSerializer
from rest_framework.serializers import Serializer

@pytest.mark.django_db
def test_comment_serializer() -> None:
    """
    Test the CommentSerializer to ensure that the serialized data for a comment 
    includes the correct user, post, and comment details.

    This test ensures that the serializer correctly serializes the comment object, 
    including the user and post data in the expected format.
    """
    user = CustomUser.objects.create(
        email="test@example.com", 
        first_name="Test", 
        last_name="User"
    )       
    post = Post.objects.create(
        user=user, 
        image="test.jpg", 
        caption="Test caption"
    )  

    comment = Comment.objects.create(
        user=user, 
        post=post, 
        text="Test comment"
    )
    serializer = CommentSerializer(
        comment
    )
    data = serializer.data
    

    assert data["id"] == comment.id
    assert data["text"] == "Test comment"
    assert data["user"]["email"] == "test@example.com"
    assert data["user"]["name"] == "Test User"
    assert data["post"]["caption"] == "Test caption"
    assert "image" in data["post"]
