from django.urls import path
from likes.views import *

urlpatterns = [
    # Comment like endpoints
    path(
        "api/comments/<int:comment_id>/like/", 
        CommentLikeToggleAPIView.as_view(), 
        name="toggle-like"
    ),
]
