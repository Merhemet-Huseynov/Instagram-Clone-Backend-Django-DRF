import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from typing import Any, Dict

from comments.models import Comment
from comments.serializers import CommentSerializer
from posts.models import Post

__all__ = [
    "CommentCreateAPIView",
    "CommentListAPIView"
]

logger = logging.getLogger(__name__)


class CommentCreateAPIView(APIView):
    """
    API to create a new comment for a post.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Create a new comment",
        responses={
            status.HTTP_201_CREATED: CommentSerializer,
            status.HTTP_400_BAD_REQUEST: openapi.Response("Invalid data", CommentSerializer),
        },
        request_body=CommentSerializer,
    )
    def post(self, request: Any, post_id: int) -> Response:
        """
        Creates a new comment for a given post.

        Args:
            request: The HTTP request containing comment data.
            post_id: The ID of the post to which the comment will be added.

        Returns:
            A Response object containing the comment data or error message.
        """
        post = get_object_or_404(Post, id=post_id)
        serializer = CommentSerializer(data=request.data, context={"request": request})

        if serializer.is_valid():
            serializer.save(post=post, user=request.user)
            logger.info(f"User {request.user.id} created a comment for post {post_id}.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        logger.error(f"Comment creation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentListAPIView(APIView):
    """
    API to retrieve all comments for a specific post.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve all comments for a post",
        responses={
            status.HTTP_200_OK: CommentSerializer(many=True),
            status.HTTP_404_NOT_FOUND: "Post not found"
        }
    )
    def get(self, request: Any, post_id: int) -> Response:
        """
        Retrieves all comments for a given post.

        Args:
            request: The HTTP request.
            post_id: The ID of the post for which comments are retrieved.

        Returns:
            A Response object containing a list of comments.
        """
        post = get_object_or_404(Post, id=post_id)
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        logger.info(f"Retrieved comments for post {post_id}.")
        return Response(serializer.data, status=status.HTTP_200_OK)
