from django.urls import include, path

urlpatterns = [
    path("", include("likes.urls.post_likes")),
    path("", include("likes.urls.comment_likes")),
    path("", include("likes.urls.story_likes")),
]
