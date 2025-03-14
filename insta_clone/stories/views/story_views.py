import logging
from rest_framework.views import APIView, Response, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from stories.models import Story
from users.models import Follow
from stories.serializers import StorySerializer
from django.utils import timezone

__all__ = [
    "StoryCreateAPIView",
    "ActiveStoriesAPIView"
]

logger = logging.getLogger(__name__)


class StoryCreateAPIView(APIView):
    """
    API view to create a new story with an image or video.
    Requires user authentication and accepts multi-part form data for story creation.
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Create a new story with image or video.",
        request_body=StorySerializer,
        responses={status.HTTP_201_CREATED: StorySerializer}
    )
    def post(self, request, *args, **kwargs) -> Response:
        """
        Handle the creation of a new story by an authenticated user.

        Args:
            request: The HTTP request containing the story data.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A response containing the created story data or error details.
        """
        serializer = StorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            logger.info(f"Story created successfully by user {request.user.id}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        logger.warning(f"Failed to create story. Errors: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ActiveStoriesAPIView(APIView):
    """
    API view to retrieve active stories from users that the current user follows.
    Requires user authentication.
    """
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Retrieve active stories from followed users.",
        responses={status.HTTP_200_OK: StorySerializer(many=True)}
    )
    def get(self, request, *args, **kwargs) -> Response:
        """
        Retrieve active stories from the users the current user follows.

        Args:
            request: The HTTP request.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            Response: A response containing a list of active stories.
        """
        user = request.user
        
        # Find the users that the current user is following
        followed_users = Follow.objects.filter(
            follower=user).values_list("followed", flat=True)
        
        # Retrieve the active stories from the followed users
        active_stories = Story.objects.filter(
            user__in=followed_users, 
            expires_at__gte=timezone.now()
        )
        serializer = StorySerializer(active_stories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
