from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from django.http import JsonResponse
from drf_yasg import openapi
import logging

from posts.models import Post
from likes.models import PostLike

__all__ = [
    "LikeToggleAPIView"
]

# Logger conf
logger = logging.getLogger(__name__)


class LikeToggleAPIView(APIView):
    """
    API endpoint to like or unlike a post.

    Users can toggle the like status of a post. If the 
    post is already liked by the user,
    the like is removed. If not, a new like is added.

    - **Authenticated users only**
    - **POST request required**
    - **Returns 201 if liked, 200 if unliked, 404 if post not found**
    """

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Like/unlike a post",
        responses={
            201: openapi.Response("Post liked."),
            200: openapi.Response("Post unliked."),
            404: openapi.Response("Post not found."),
        },
    )
    def post(self, request: Request, post_id: int) -> JsonResponse:
        """
        Toggle the like status on a post.

        Args:
            request (Request): The HTTP request object.
            post_id (int): The ID of the post to like/unlike.

        Returns:
            JsonResponse: A JSON response indicating the action taken.
        """
        logger.info(f"User {request.user.id} is attempting to like/unlike post {post_id}.")

        post: Post = get_object_or_404(Post, id=post_id)
        
        was_liked: bool = PostLike.toggle_like(request.user, post)

        if was_liked:
            logger.info(f"User {request.user.id} liked post {post.id}.")
            return Response({"detail": "Post liked."}, status=status.HTTP_201_CREATED)
        
        logger.info(f"User {request.user.id} unliked post {post.id}.")
        return Response({"detail": "Post unliked."}, status=status.HTTP_200_OK)
