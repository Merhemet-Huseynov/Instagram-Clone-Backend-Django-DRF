from django.contrib import admin
from django.utils.timezone import localtime, timedelta
from users.models import VerificationCode


@admin.register(VerificationCode)
class VerificationCodeAdmin(admin.ModelAdmin):
    """
    Admin interface for managing verification codes.
    Allows marking codes as verified and deleting expired codes.
    """
    
    list_display = (
        "get_email",
        "verification_code",
        "is_verified",
        "local_created_at",
        "is_expired_display",
    )
    list_filter = (
        "is_verified", 
        "created_at"
    )
    search_fields = (
        "user__email", 
        "verification_code"
    ) 
    readonly_fields = (
        "created_at",
    )

    actions = ["mark_as_verified", "delete_expired_codes"]

    def get_email(self, obj: VerificationCode) -> str:
        """
        Return the email of the associated user.
        """
        return obj.user.email

    get_email.short_description = "Email"
    get_email.admin_order_field = "user__email"

    def local_created_at(self, obj: VerificationCode) -> str:
        """
        Return the local time of when the verification code was created.
        """
        return localtime(obj.created_at).strftime("%Y-%m-%d %H:%M:%S")

    local_created_at.admin_order_field = "created_at"
    local_created_at.short_description = "Local Time"

    def is_expired_display(self, obj: VerificationCode) -> bool:
        """
        Display whether the verification code is expired.
        """
        return obj.is_expired()

    is_expired_display.short_description = "Expired?"
    is_expired_display.boolean = True

    @admin.action(description="Mark selected codes as verified")
    def mark_as_verified(self, request, queryset):
        """
        Mark selected verification codes as verified.
        """
        updated_count = queryset.update(is_verified=True)
        self.message_user(request, f"{updated_count} verification codes marked as verified.")

    @admin.action(description="Delete expired verification codes")
    def delete_expired_codes(self, request, queryset):
        """
        Delete expired verification codes based on the 3-minute expiration rule.
        """
        expired_codes = queryset.filter(created_at__lt=localtime() - timedelta(seconds=180))
        deleted_count, _ = expired_codes.delete()
        self.message_user(request, f"{deleted_count} expired verification codes deleted.")
