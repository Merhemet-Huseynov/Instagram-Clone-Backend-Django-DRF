from django.urls import path
from likes.views import *

urlpatterns = [
    # Comment endpoints
    path(
        "api/comments/<int:comment_id>/like/", 
        LikeToggleAPIView.as_view(), 
        name="toggle-like"
    ),
]
