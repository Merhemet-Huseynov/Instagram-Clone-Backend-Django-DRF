import logging
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView, Response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from drf_yasg import openapi

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
    View for updating a user's profile with support for multipart form data.
    
    This view allows users to update their first name, last name, bio, and profile picture.
    It supports multipart form data format (image uploads).
    """

    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser] 

    @swagger_auto_schema(
        request_body=UpdateProfileSerializer,
        responses={
            status.HTTP_200_OK: openapi.Response(
                description="Profile updated successfully",
                schema=UpdateProfileSerializer,
            ),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Invalid input or failed validation"
            ),
        },
    )
    def put(self, request, *args, **kwargs):
        """
        Updates the user profile with the provided data.
        
        Only the authenticated user can update their own profile.
        """
        user = request.user  # Get the current authenticated user
        
        # Deserialize the incoming request data using the UpdateProfileSerializer
        serializer = UpdateProfileSerializer(
            user, data=request.data
        )
        
        # Validate the data
        if serializer.is_valid():
            # Save the updated profile
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Return validation errors if any
        return Response(
            serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )
