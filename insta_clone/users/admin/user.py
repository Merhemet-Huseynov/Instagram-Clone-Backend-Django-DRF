from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import mark_safe
from django.contrib.auth.models import User

from ..forms import CustomUserCreationForm, CustomUserChangeForm
from ..models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for the CustomUser model.

    This class defines how the CustomUser model is presented in the Django admin panel,
    including displaying the profile picture preview and bio fields, as well as handling 
    user creation and modification forms.
    """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    def profile_picture_preview(self, obj: CustomUser) -> str:
        """
        Generates an HTML preview for the user's profile picture in the admin list view.

        Args:
            obj (CustomUser): The user instance.

        Returns:
            str: HTML markup for the image preview or a placeholder text if no image is set.
        """
        if obj.profile_picture:
            return mark_safe(f'<img src="{obj.profile_picture.url}" width="50" height="50" />')
        return "No image"
    
    profile_picture_preview.short_description = "Profile Picture Preview"

    list_display = ("email", "profile_picture_preview", "is_staff", "is_active",)
    list_filter = ("email", "is_staff", "is_active",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("profile_picture", "bio")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions"
            )}
        ),
    )

    search_fields = ("email",)
    ordering = ("email",)



