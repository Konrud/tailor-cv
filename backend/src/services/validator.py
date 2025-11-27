"""Validation service for file size, format, and anti-fabrication checks.

This module provides validation logic for uploaded files and generated content
to ensure compliance with functional requirements.
"""

from pathlib import Path

from src.utils.config import settings
from src.utils.errors import FabricationError, ValidationError


def validate_file_size(file_size: int) -> None:
    """Validate file size does not exceed configured limit (FR-001a).

    Args:
        file_size: File size in bytes

    Raises:
        ValidationError: If file size exceeds limit
    """
    if file_size > settings.max_file_size_bytes:
        raise ValidationError(
            f"File size exceeds {settings.max_file_size_mb} MB limit",
            details=f"File size: {file_size} bytes, Max: {settings.max_file_size_bytes} bytes",
        )


def validate_file_format(filename: str, content_type: str | None = None) -> str:
    """Validate file format is PDF, DOCX, or TXT (FR-001b).

    Args:
        filename: Name of the uploaded file
        content_type: MIME type of the file (optional)

    Returns:
        str: Normalized file extension ("pdf", "docx", or "txt")

    Raises:
        ValidationError: If file format is not supported
    """
    allowed_extensions = {".pdf", ".docx", ".txt"}
    allowed_content_types = {
        "application/pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "text/plain",
    }

    file_extension = Path(filename).suffix.lower()

    if file_extension not in allowed_extensions:
        raise ValidationError(
            "Invalid file format. Please upload a PDF, DOCX, or TXT file.",
            details=f"File extension: {file_extension}",
        )

    # Additional content type validation if provided
    if content_type and content_type not in allowed_content_types:
        raise ValidationError(
            "Invalid file content type.",
            details=f"Content type: {content_type}",
        )

    # Return normalized extension without dot
    return file_extension.lstrip(".")


def validate_page_count(page_count: int) -> None:
    """Validate document page count does not exceed limit (FR-027).

    Args:
        page_count: Number of pages in the document

    Raises:
        ValidationError: If page count exceeds limit
    """
    if page_count > settings.max_page_count:
        raise ValidationError(
            f"Document exceeds {settings.max_page_count} pages limit",
            details=f"Page count: {page_count}",
        )


def validate_word_count(word_count: int) -> None:
    """Validate text word count does not exceed limit (FR-028).

    Args:
        word_count: Number of words in the text

    Raises:
        ValidationError: If word count exceeds limit
    """
    if word_count > settings.max_word_count:
        raise ValidationError(
            f"Text exceeds {settings.max_word_count} words limit",
            details=f"Word count: {word_count}",
        )


def validate_anti_fabrication(original_text: str, tailored_text: str, threshold: float = 0.7) -> None:
    """Validate tailored CV content against original to prevent fabrication (FR-010b).

    This function performs a basic validation to ensure all claims in the tailored CV
    can be traced back to the original CV content.

    Args:
        original_text: Original CV text
        tailored_text: Tailored CV text
        threshold: Similarity threshold (0.0 to 1.0)

    Raises:
        FabricationError: If fabricated content is detected
    """
    # Extract claims from tailored CV (simple implementation - extract bullet points)
    tailored_claims = [
        line.strip()
        for line in tailored_text.split("\n")
        if line.strip().startswith(("•", "-", "*", "○"))
    ]

    original_lower = original_text.lower()
    fabricated_claims = []

    for claim in tailored_claims:
        # Remove bullet point and clean the claim
        clean_claim = claim.lstrip("•-*○ ").strip().lower()

        # Check if key phrases from claim exist in original
        # This is a simple keyword-based check
        words = clean_claim.split()
        if len(words) < 3:  # Skip very short claims
            continue

        # Extract key words (skip common words)
        stop_words = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
        }
        key_words = [w for w in words if w not in stop_words and len(w) > 3]

        # Count how many key words exist in original
        if key_words:
            matches = sum(1 for word in key_words if word in original_lower)
            match_ratio = matches / len(key_words)

            if match_ratio < threshold:
                fabricated_claims.append(clean_claim[:100])  # Truncate for error message

    if fabricated_claims:
        raise FabricationError(
            "Tailored CV contains claims that cannot be verified in the original CV",
            details=f"Suspicious claims: {fabricated_claims[:3]}",  # Show first 3
        )

