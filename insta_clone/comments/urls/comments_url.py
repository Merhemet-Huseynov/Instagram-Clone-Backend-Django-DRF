from django.urls import path
from comments.views import *

urlpatterns = [
    # Comment endpoints
    path(
        "comments/posts/<int:post_id>/comment/", 
        CommentCreateAPIView.as_view(), 
        name="create_comment"
    ),
    
    path(
        "comments/posts/<int:post_id>/comments/", 
        CommentListAPIView.as_view(), 
        name="list_comments"
    ),
]