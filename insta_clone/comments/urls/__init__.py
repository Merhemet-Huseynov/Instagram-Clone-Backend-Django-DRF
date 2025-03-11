from django.urls import include, path

urlpatterns = [
    path("", include("comments.urls.comments_url")),
]
