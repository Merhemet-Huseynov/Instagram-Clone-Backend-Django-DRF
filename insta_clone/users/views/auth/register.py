import logging
from rest_framework.views import APIView, Response, status
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema

from users.serializers.auth import RegisterSerializer

__all__ = ["RegisterView"]

logger = logging.getLogger(__name__) 

User = get_user_model() 


class RegisterView(APIView):

    @swagger_auto_schema(request_body=RegisterSerializer)
    def post(self, request):
        logger.info("Registration request received with data: %s", request.data)  

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            logger.info("Registration successful for user: %s", user.username) 
            return Response({
                "message": "Registration successful."
                }, status=status.HTTP_201_CREATED
            )

        logger.warning("Registration failed: %s", serializer.errors)
        return Response(
            serializer.errors, 
            status=status.HTTP_400_BAD_REQUEST
        )
