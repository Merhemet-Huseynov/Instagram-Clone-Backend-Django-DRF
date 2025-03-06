import logging
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404

from users.models import CustomUser
from users.serializers import UserSerializer, UpdateProfileSerializer

__all__ = [
    "UserProfileView",
    "UpdateProfileView"
]

# Set up logging
logger = logging.getLogger(__name__)


class UserProfileView(APIView):
    """
    API view to retrieve user profile details.
    
    This view is accessible only to authenticated users. It fetches the user's profile based
    on the provided username (slug) and returns the user data.
    """
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_description="Get user profile details",
        responses={200: UserSerializer()},
    )
    def get(self, request, username: str, *args, **kwargs) -> Response:
        """
        Retrieves the profile of a user by username.

        Args:
            request: The HTTP request.
            username (str): The username (slug) of the user whose profile is being fetched.

        Returns:
            Response: The serialized user data, or an error if the user is not found.
        """
        user = get_object_or_404(CustomUser, slug=username)
        serializer = UserSerializer(user)
        logger.info(f"Fetched profile for user: {username}")
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class UpdateProfileView(APIView):
    """
    API view to update the authenticated user's profile.

    This view is accessible only to authenticated users and allows the user to update 
    their profile details, including profile picture, bio, etc.
    """

    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated]
    
    def get_object(self) -> CustomUser:
        """
        Retrieves the currently authenticated user.

        Returns:
            CustomUser: The currently authenticated user.
        """
        return self.request.user

    @swagger_auto_schema(
        request_body=UpdateProfileSerializer,
        operation_description="User profile update endpoint",
        consumes=["multipart/form-data"]
    )
    def put(self, request, *args, **kwargs) -> Response:
        """
        Updates the profile of the authenticated user.

        Args:
            request: The HTTP request containing the updated profile data.

        Returns:
            Response: The updated user profile data, or an error if the data is invalid.
        """
        user = self.get_object()
        serializer = UpdateProfileSerializer(user, data=request.data)

        if serializer.is_valid():
            serializer.save()
            logger.info(f"User profile updated for user: {user.username}")
            return Response(serializer.data, status=status.HTTP_200_OK)

        logger.error(f"Failed to update profile for user: {user.username} - {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
