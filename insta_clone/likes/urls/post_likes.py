from django.urls import path
from likes.views import *

urlpatterns = [
    # PostLike endpoints
    path(
        "likes/posts/<int:post_id>/like/", 
        LikeToggleAPIView.as_view(), 
        name="toggle-like"
    ),
]
