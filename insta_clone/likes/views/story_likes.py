import logging
from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from stories.models import Story
from likes.models import StoryLike

__all__ = [
    "StoryLikeToggleAPIView",
]

logger = logging.getLogger(__name__)


class StoryLikeToggleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Like/unlike a story",
        responses={
            201: openapi.Response("Story liked."),
            200: openapi.Response("Story unliked."),
            404: openapi.Response("Story not found."),
        },
    )
    def post(self, request, story_id: int) -> Response:
        """
        Toggle the like status on a story.

        This view allows an authenticated user to like or unlike a story. If the user
        likes the story, a new like is created; if the user unlikes it, the like is removed.

        Returns:
            Response: A response indicating the action taken, either like or unlike.
        """
        story = get_object_or_404(Story, id=story_id)

        try:
            was_liked = StoryLike.toggle_like(request.user, story)
        except IntegrityError as e:
            logger.error(f"Database integrity error while toggling like for story {story_id}: {e}")
            return Response(
                {"detail": "Database error occurred."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except Exception as e:
            logger.error(f"Unexpected error while toggling like for story {story_id}: {e}")
            return Response(
                {"detail": "An unexpected error occurred."}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        if was_liked:
            logger.info(f"User {request.user} liked story {story_id}")
            return Response({"detail": "Story liked."}, status=status.HTTP_201_CREATED)

        logger.info(f"User {request.user} unliked story {story_id}")
        return Response({"detail": "Story unliked."}, status=status.HTTP_200_OK)
