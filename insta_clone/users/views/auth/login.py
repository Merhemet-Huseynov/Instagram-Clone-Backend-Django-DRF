import logging
from rest_framework.views import APIView, Response, status
from drf_yasg.utils import swagger_auto_schema

from users.serializers.auth import LoginSerializer

__all__ = ["LoginView"]

logger = logging.getLogger(__name__)  


class LoginView(APIView):
    """
    View to handle user login requests.

    This view allows users to log in by providing their credentials in the request body.
    It uses a `LoginSerializer` to validate the provided data and return appropriate responses.
    """

    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request) -> Response:
        """
        Handles the POST request to log in a user.

        Args:
            request: The HTTP request containing user credentials.

        Returns:
            Response: A Response object containing the result of the login attempt.
        """
        logger.info("Login request received")  

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            logger.info("Login successful") 
            return Response(
                serializer.validated_data, 
                status=status.HTTP_200_OK
            )
        
        logger.warning("Login failed: %s", serializer.errors) 
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )