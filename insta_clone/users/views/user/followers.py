import logging
from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

from users.models import Follow
from users.models import CustomUser
from users.serializers.user import FollowSerializer

__all__ = ["FollowToggleView"]

# Configure logger
logger = logging.getLogger(__name__)


class FollowToggleView(APIView):
    """
    API view to toggle follow/unfollow status for a user.

    This view allows authenticated users to follow or unfollow another user.
    If the user tries to follow themselves, an error is returned.
    If the user is not found, a 404 error is returned.

    Methods:
        POST: Toggles follow/unfollow status for the specified user.
    """
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Toggle follow/unfollow user",
        responses={200: "Follow toggled successfully", 400: "Invalid request"}
    )
    def post(self, request, username: str) -> Response:
        """
        Handles the POST request to toggle follow/unfollow status for a user.

        Args:
            request: The HTTP request object.
            username: The username (slug) of the user to follow/unfollow.

        Returns:
            Response: The HTTP response object containing the result of the operation.
        """
        try:
            # Log the attempt to follow/unfollow
            logger.info(f"User {request.user.username} is attempting to follow/unfollow {username}.")

            # Retrieve the followed user by their slug
            followed_user = CustomUser.objects.get(slug=username)

            # Check if the user is trying to follow themselves
            if request.user == followed_user:
                logger.warning(f"User {request.user.username} attempted to follow themselves.")
                return Response(
                    {"error": "You cannot follow yourself"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Toggle follow/unfollow status
            followed = Follow.toggle_follow(request.user, followed_user)

            # Log success or failure
            action = "Followed" if followed else "Unfollowed"
            logger.info(f"User {request.user.username} has {action} {followed_user.username} successfully.")

            return Response(
                {"message": f"{action} successfully"},
                status=status.HTTP_200_OK
            )
        except CustomUser.DoesNotExist:
            logger.error(f"User {username} not found.")
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
