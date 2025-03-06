from django.urls import include, path

urlpatterns = [
    path("", include("users.urls.auth")),
    path("", include("users.urls.password")),
    path("", include("users.urls.verfication")),
    path("", include("users.urls.user"))
]