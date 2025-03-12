from django.urls import path
from users.views import *

urlpatterns = [
    # Password endpoints
    path(
        "users/reset-password-send-code/", 
        ResetPasswordSendCodeView.as_view(), 
        name="reset-password-send-code"
    ),

    path(
        "users/reset-password/", 
        ResetPasswordView.as_view(), 
        name="reset-password"
    ),
    
    path(
        "users/change-password/",
        ChangePasswordView.as_view(), 
        name="change-password"
    ),
]