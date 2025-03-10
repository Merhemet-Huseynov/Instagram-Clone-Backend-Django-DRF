from django.urls import include, path

urlpatterns = [
    path("", include("likes.urls.like")),
]
