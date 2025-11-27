"""Pydantic models for CV data structures.

This module defines the data models for CV parsing, validation, and processing.
"""

from datetime import datetime
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class CVSection(BaseModel):
    """A single section within a CV (e.g., experience, education, skills)."""

    type: Literal["summary", "experience", "education", "skills", "certifications", "other"]
    title: str = Field(..., max_length=200, description="Section heading")
    content: str = Field(..., max_length=10000, description="Section full text")
    items: list[str] = Field(
        default_factory=list, description="Bullet points or list items in this section"
    )


class MasterCV(BaseModel):
    """The user's original uploaded CV with parsed content.

    This represents the master CV that will be tailored for specific job descriptions.
    Validation ensures compliance with FR-001, FR-025, FR-027.
    """

    id: UUID = Field(default_factory=uuid4)
    file_name: str = Field(..., max_length=255)
    file_type: Literal["pdf", "docx", "txt"]
    file_size: int = Field(..., le=5_242_880, description="File size in bytes (max 5 MB)")
    uploaded_at: datetime = Field(default_factory=datetime.utcnow)
    extracted_text: str = Field(
        ..., min_length=10, max_length=100000, description="Plain text extracted from file"
    )
    parsed_sections: list[CVSection] = Field(
        ..., description="Structured sections parsed from CV"
    )
    language: Literal["en"] = Field(default="en", description="English only per FR-025")
    page_count: int = Field(..., le=5, ge=1, description="Number of pages (max 5 per FR-027)")

    @field_validator("file_size")
    @classmethod
    def validate_file_size(cls, v: int) -> int:
        """Validate file size does not exceed 5 MB (FR-001a)."""
        if v > 5_242_880:  # 5 MB in bytes
            raise ValueError("File size exceeds 5 MB limit (FR-001a)")
        return v

    @field_validator("page_count")
    @classmethod
    def validate_page_count(cls, v: int) -> int:
        """Validate page count does not exceed 5 pages (FR-027)."""
        if v > 5:
            raise ValueError("CV exceeds 5 pages limit (FR-027)")
        return v

