from django.urls import path, include

urlpatterns = [
    path("likes/", include("posts.urls"))
]