from django.urls import path
from likes.views import *

urlpatterns = [
    # Like endpoints
    path(
        "api/posts/<int:post_id>/like/", 
        LikeToggleAPIView.as_view(), 
        name="toggle-like"
    ),
]
