import re
import logging
from typing import Dict

__all__ = ["convert_to_slug"]

logger = logging.getLogger(__name__)


AZERBAIJANI_TO_LATIN: Dict[str, str] = {
    "ş": "s",
    "ə": "e", 
    "ı": "i", 
    "ç": "c", 
    "ğ": "g", 
    "ö": "o", 
    "ü": "u",
    "Ş": "S", 
    "Ə": "E", 
    "İ": "I", 
    "Ç": "C", 
    "Ğ": "G", 
    "Ö": "O", 
    "Ü": "U"
}

def convert_to_slug(text: str) -> str:
    """
    Converts Azerbaijani text to a URL-friendly slug.

    Steps:
    1. Replace Azerbaijani-specific characters with their Latin equivalents.
    2. Convert the text to lowercase.
    3. Replace non-alphanumeric characters (except "-") with "-".
    4. Ensure that multiple dashes are replaced with a single dash.
    5. Trim leading and trailing dashes.

    Args:
        text (str): The input text to convert.

    Returns:
        str: The generated slug.
    """
    logger.info(f"Converting text to slug: {text}")

    for az_letter, lat_letter in AZERBAIJANI_TO_LATIN.items():
        text = text.replace(az_letter, lat_letter)

    text = text.lower()
    text = re.sub(r"-{2,}", "-", re.sub(r"[^a-z0-9-]", "-", text))

    result = text.strip("-")
    
    logger.info(f"Converted slug: {result}")
    return result