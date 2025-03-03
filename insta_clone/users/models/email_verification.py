from django.db import models
from django.utils.timezone import now
from django.contrib.auth import get_user_model

User = get_user_model()


class VerificationCode(models.Model):
    """
    Model for storing email verification codes.
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name="verification_codes"
    )
    email = models.EmailField(
        unique=True
    ) 
    verification_code = models.CharField(
        max_length=6
    )
    is_verified = models.BooleanField(
        default=False
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["verification_code"]),
        ]

    def __str__(self) -> str:
        return f"Verification code for {self.email}"

    def is_expired(self) -> bool:
        """
        Checks if the verification code has expired (3 minutes).
        """
        return (now() - self.created_at).total_seconds() > 180
