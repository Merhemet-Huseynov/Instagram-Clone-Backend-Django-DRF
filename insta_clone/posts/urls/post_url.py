from django.urls import path
from posts.views import *

urlpatterns = [
    # Post endpoints
    path(
        "posts/post-list/", 
        PostListAPIView.as_view(), 
        name="post-list"
    ),

    path(
        "posts/post-create/", 
        PostCreateAPIView.as_view(), 
        name="post-create"
    ),
    
    path(
        "posts/<int:id>/", 
        PostDetailAPIView.as_view(), 
        name="post-detail"
    ),

    path(
        "posts/<int:id>/delete/", 
        PostDeleteAPIView.as_view(), 
        name="post-delete"
    ),
]
