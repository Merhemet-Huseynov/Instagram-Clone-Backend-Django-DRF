from django.urls import path
from likes.views import *

urlpatterns = [
    # StoryLike endpoints
    path(
        "likes/stories/<int:story_id>/like/", 
        StoryLikeToggleAPIView.as_view(), 
        name="toggle-story-like"
    ),
]
