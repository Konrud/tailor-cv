"""Configuration management for AI CV Tailor backend.

This module provides centralized configuration loading from environment variables
using Pydantic Settings for type safety and validation.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"

    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True

    # CORS Configuration
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    # Processing Limits
    max_file_size_mb: int = 5
    max_page_count: int = 5
    max_word_count: int = 2500
    url_timeout_seconds: int = 10

    # Retry Configuration
    max_retries: int = 3
    retry_delay_seconds: int = 1
    retry_backoff_factor: int = 2

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins from comma-separated string."""
        return [origin.strip() for origin in self.cors_origins.split(",")]

    @property
    def max_file_size_bytes(self) -> int:
        """Convert max file size from MB to bytes."""
        return self.max_file_size_mb * 1024 * 1024


# Global settings instance
settings = Settings()

