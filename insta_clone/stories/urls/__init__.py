from django.urls import path, include

urlpatterns = [
    path("", include("stories.urls.story_url"))
]