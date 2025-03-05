from django.urls import path
from users.views import *

urlpatterns = [
    # Password endpoints
    path(
        "reset-password-send-code/", 
        ResetPasswordSendCodeView.as_view(), 
        name="reset-password-send-code"
    ),

    path(
        "reset-password/", 
        ResetPasswordView.as_view(), 
        name="reset-password"
    ),
    
    path(
        "change-password/",
        ChangePasswordView.as_view(), 
        name="change-password"
    ),
]