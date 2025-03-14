from django.urls import path
from stories.views import *

urlpatterns = [
    # Story endpoints
    path(
        "stories/", 
        StoryCreateAPIView.as_view(), 
        name="create-story"
    ),
    path(
        "stories/active/", 
        ActiveStoriesAPIView.as_view(), 
        name="active-stories"
    ),
]
