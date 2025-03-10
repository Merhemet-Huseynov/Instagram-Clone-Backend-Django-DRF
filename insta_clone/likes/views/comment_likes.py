import logging
from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from comments.models import Comment
from likes.models import CommentLike

__all__ = [
    "CommentLikeToggleAPIView"
]

# Setting up the logger
logger = logging.getLogger(__name__)


class CommentLikeToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Like/unlike a comment",
        responses={
            201: openapi.Response("Comment liked."),
            200: openapi.Response("Comment unliked."),
            404: openapi.Response("Comment not found."),
        },
    )
    def post(self, request, comment_id: int) -> Response:
        """
        Toggle the like status on a comment.

        This view allows an authenticated user to like or unlike a comment. If the user
        likes the comment, a new like is created; if the user unlikes it, the like is removed.

        Args:
            request (Request): The HTTP request object.
            comment_id (int): The ID of the comment to like/unlike.

        Returns:
            Response: A response indicating the action taken, either like or unlike.
        """
        comment = get_object_or_404(Comment, id=comment_id)
        
        try:
            was_liked = CommentLike.toggle_like(request.user, comment)
        except Exception as e:
            logger.error(f"Error toggling like for comment {comment_id}: {e}")
            return Response(
                {"detail": "An error occurred while toggling like."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        if was_liked:
            logger.info(f"User {request.user} liked comment {comment_id}")
            return Response({"detail": "Comment liked."}, status=status.HTTP_201_CREATED)

        logger.info(f"User {request.user} unliked comment {comment_id}")
        return Response({"detail": "Comment unliked."}, status=status.HTTP_200_OK)
