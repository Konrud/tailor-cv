"""Language detection service for validating English content.

This module provides language detection functionality using langdetect
to ensure uploaded CVs and job descriptions are in English (FR-025, FR-026).
"""

from langdetect import LangDetectException, detect, detect_langs

from src.utils.errors import LanguageDetectionError


def detect_language(text: str, min_confidence: float = 0.8) -> str:
    """Detect the language of given text.

    Args:
        text: Text content to analyze
        min_confidence: Minimum confidence threshold (0.0 to 1.0)

    Returns:
        str: Detected language code (e.g., "en", "es", "fr")

    Raises:
        LanguageDetectionError: If language detection fails or confidence is too low
    """
    if not text or len(text.strip()) < 10:
        raise LanguageDetectionError(
            "Text is too short for reliable language detection",
            details=f"Text length: {len(text)} characters",
        )

    try:
        # Get language with confidence scores
        lang_probs = detect_langs(text)

        # Get the most probable language
        top_lang = lang_probs[0]
        detected_lang = top_lang.lang
        confidence = top_lang.prob

        # Check confidence threshold
        if confidence < min_confidence:
            raise LanguageDetectionError(
                f"Language detection confidence too low ({confidence:.2f})",
                details=f"Detected: {detected_lang}, Confidence: {confidence:.2f}",
            )

        return detected_lang

    except LangDetectException as e:
        raise LanguageDetectionError(
            "Failed to detect language",
            details=str(e),
        ) from e


def validate_english(text: str) -> None:
    """Validate that the text is in English (FR-025, FR-026).

    Args:
        text: Text content to validate

    Raises:
        LanguageDetectionError: If text is not in English
    """
    detected_lang = detect_language(text)

    if detected_lang != "en":
        raise LanguageDetectionError(
            "Only English language CVs and job descriptions are supported",
            details=f"Detected language: {detected_lang}",
        )


def is_english(text: str) -> bool:
    """Check if text is in English without raising exceptions.

    Args:
        text: Text content to check

    Returns:
        bool: True if text is in English, False otherwise
    """
    try:
        validate_english(text)
        return True
    except LanguageDetectionError:
        return False

