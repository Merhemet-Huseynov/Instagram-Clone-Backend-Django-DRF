import logging
from rest_framework.views import APIView, Response, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import permissions
from django.shortcuts import get_object_or_404
from posts.permissions import IsOwnerOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from posts.models import Post
from users.models import Follow
from posts.serializers import PostSerializer

# Configure logging
logger = logging.getLogger(__name__)

__all__ = [
    "PostCreateAPIView",
    "PostListAPIView",
    "PostDetailAPIView",
    "PostDeleteAPIView"
]


class PostCreateAPIView(APIView):
    """
    API view to create a new post with an image and text.
    Only authenticated users can create posts.
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Create a new post",
        request_body=PostSerializer,
        responses={status.HTTP_201_CREATED: PostSerializer}
    )
    def post(self, request, *args, **kwargs) -> Response:
        """
        Handles POST requests to create a new post.

        Args:
            request: The incoming HTTP request containing the post data.

        Returns:
            Response: A response containing the created post's data or error messages.
        """
        serializer = PostSerializer(
            data=request.data, 
            context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(user=request.user)
            logger.info(f"Post created successfully by user {request.user.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        logger.warning(f"Failed to create post. Errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostListAPIView(APIView):
    """
    API view to list posts from followed users.
    Only authenticated users can view the posts.
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve posts from followed users",
        responses={status.HTTP_200_OK: PostSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs) -> Response:
        """
        Handles GET requests to retrieve posts from followed users.

        Args:
            request: The incoming HTTP request.

        Returns:
            Response: A response containing the list of posts from followed users.
        """
        user = request.user
        followed_users = Follow.objects.filter(follower=user).values_list("followed__id", flat=True)
        posts = Post.objects.filter(user_id__in=followed_users).order_by("-created_at")
        logger.info(f"Fetched {posts.count()} posts from followed users for user {user.id}")
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostDetailAPIView(APIView):
    """
    API view to retrieve the details of a specific post.
    Only authenticated users can view the post details.
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve post details by ID",
        responses={status.HTTP_200_OK: PostSerializer}
    )
    def get(self, request, id: int, *args, **kwargs) -> Response:
        """
        Handles GET requests to retrieve a post's details by its ID.

        Args:
            request: The incoming HTTP request.
            id: The ID of the post to retrieve.

        Returns:
            Response: A response containing the post's details.
        """
        post = get_object_or_404(Post, id=id)
        logger.info(f"Retrieved details for post {id}")
        serializer = PostSerializer(post)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PostDeleteAPIView(APIView):
    """
    API view to delete a specific post.
    Only the owner of the post can delete it.
    """
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    @swagger_auto_schema(
        operation_description="Delete a post by ID",
        responses={status.HTTP_204_NO_CONTENT: "Post deleted successfully"}
    )
    def delete(self, request, id: int, *args, **kwargs) -> Response:
        """
        Handles DELETE requests to delete a post by its ID.

        Args:
            request: The incoming HTTP request.
            id: The ID of the post to delete.

        Returns:
            Response: A response indicating the success or failure of the deletion.
        """
        post = get_object_or_404(Post, id=id)
        self.check_object_permissions(request, post)
        post.delete()
        logger.info(f"Post {id} deleted successfully by user {request.user.id}")
        return Response(status=status.HTTP_204_NO_CONTENT)