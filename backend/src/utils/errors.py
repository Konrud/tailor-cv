"""Custom exception classes for AI CV Tailor backend.

This module defines domain-specific exceptions for better error handling
and user-friendly error messages.
"""


class CVTailorError(Exception):
    """Base exception for all AI CV Tailor errors."""

    def __init__(self, message: str, details: str | None = None) -> None:
        """Initialize with message and optional details.

        Args:
            message: User-friendly error message
            details: Technical details for logging/debugging
        """
        self.message = message
        self.details = details
        super().__init__(self.message)


class ValidationError(CVTailorError):
    """Raised when input validation fails."""

    pass


class FileProcessingError(CVTailorError):
    """Raised when file extraction or processing fails."""

    pass


class LanguageDetectionError(CVTailorError):
    """Raised when language detection fails or detects non-English."""

    pass


class TimeoutError(CVTailorError):
    """Raised when an operation exceeds the allowed time limit."""

    pass


class URLExtractionError(CVTailorError):
    """Raised when job URL extraction fails."""

    pass


class FabricationError(CVTailorError):
    """Raised when AI-generated content contains fabricated information."""

    pass


class AIServiceError(CVTailorError):
    """Raised when OpenAI API or AI agent service fails."""

    pass


class PDFGenerationError(CVTailorError):
    """Raised when PDF generation fails."""

    pass


class RateLimitError(CVTailorError):
    """Raised when API rate limit is exceeded."""

    pass

