from django.core.exceptions import ValidationError
import imghdr
from typing import Any

def validate_image_format(image: Any) -> None:
    """
    Validates the image format.

    Only JPG and PNG formats are allowed.

    :param image: The uploaded image file
    :raises ValidationError: Raises an error if the file format is invalid.
    """
    valid_extensions = {"jpeg", "png"}
    ext = imghdr.what(image)
    if ext not in valid_extensions:
        raise ValidationError("Only JPG and PNG images are allowed.")

def validate_image_size(image: Any) -> None:
    """
    Validates the image file size.

    The maximum allowed file size is 5MB.

    :param image: The uploaded image file
    :raises ValidationError: Raises an error if the file size exceeds 5MB.
    """
    max_size = 5 * 1024 * 1024
    if image.size > max_size:
        raise ValidationError("Image size must not exceed 5MB.")
