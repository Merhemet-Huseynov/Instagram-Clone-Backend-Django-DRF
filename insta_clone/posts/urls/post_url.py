from django.urls import path
from posts.views import *

urlpatterns = [
    # Post endpoints
    path(
        "post-list/", 
        PostListAPIView.as_view(), 
        name="post-list"
    ),

    path(
        "post-create/", 
        PostCreateAPIView.as_view(), 
        name="post-create"
    ),
    
    path(
        "posts/<int:id>/", 
        PostDetailAPIView.as_view(), 
        name="post-detail"
    ),

    path(
        "post/<int:id>/delete/", 
        PostDeleteAPIView.as_view(), 
        name="post-delete"
    ),
]
