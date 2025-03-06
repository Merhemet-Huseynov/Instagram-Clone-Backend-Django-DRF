import logging
from utils.slug import convert_to_slug
from django.db import models

__all__ = ["generate_unique_slug"]

logger = logging.getLogger(__name__)


def generate_unique_slug(base_name: str, model_class: type[models.Model]) -> str:
    """
    Provides a unique slug generation based on the given model class.

    :param base_name: Base name to create the slug from
    :param model_class: Model class, e.g. Author, Category, etc.
    :return: Unique slug
    """
    logger.info(
        f"Generating slug for base name: {base_name} using model class: {model_class.__name__}"
    )

    base_slug = convert_to_slug(base_name)
    slug = base_slug
    counter = 1

    # Log if a slug already exists
    while model_class.objects.filter(slug=slug).exists():
        logger.debug(
            f"Slug \"{slug}\" already exists, generating new one with counter {counter}."
        )
        slug = f"{base_slug}-{counter}"
        counter += 1

    logger.info(f"Generated unique slug: {slug}")
    return slug