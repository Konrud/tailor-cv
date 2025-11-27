"""Pydantic models for job description data structures.

This module defines the data models for job description parsing, validation, and processing.
"""

from datetime import datetime
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class RequiredSkill(BaseModel):
    """A single skill requirement from a job description."""

    name: str = Field(..., max_length=100, description="Skill name")
    category: Literal["technical", "soft", "domain", "tool", "language"] = Field(
        ..., description="Skill category"
    )
    required: bool = Field(..., description="True if required, False if preferred")
    years_experience: int | None = Field(
        None, ge=0, le=50, description="Required years of experience if specified"
    )


class JobRequirements(BaseModel):
    """Parsed requirements from a job description."""

    title: str = Field(..., max_length=200, description="Job title")
    company: str | None = Field(None, max_length=200, description="Company name if available")
    seniority_level: str | None = Field(
        None, max_length=50, description="Seniority level (e.g., Senior, Mid-level, Entry)"
    )
    skills: list[RequiredSkill] = Field(..., description="Required and preferred skills")
    responsibilities: list[str] = Field(..., max_length=50, description="Key responsibilities")
    qualifications: list[str] = Field(..., max_length=50, description="Required qualifications")
    keywords: list[str] = Field(
        ..., max_length=100, description="Important keywords for ATS optimization"
    )


class JobDescription(BaseModel):
    """Target job description from text input or URL extraction.

    Validation ensures compliance with FR-002, FR-003, FR-026, FR-028.
    """

    id: UUID = Field(default_factory=uuid4)
    source: Literal["text", "url"] = Field(..., description="Input method")
    source_url: str | None = Field(None, max_length=2048, description="URL if from job posting")
    raw_text: str = Field(
        ..., min_length=10, max_length=50000, description="Original job description text"
    )
    extracted_at: datetime = Field(default_factory=datetime.utcnow)
    requirements: JobRequirements = Field(..., description="Parsed requirements")
    language: Literal["en"] = Field(default="en", description="English only per FR-026")
    word_count: int = Field(
        ..., le=2500, ge=1, description="Word count (max 2500 words per FR-028)"
    )
    platform: Literal["linkedin", "indeed", "glassdoor", "other"] | None = Field(
        None, description="Platform if from URL"
    )

    @field_validator("word_count")
    @classmethod
    def validate_word_count(cls, v: int) -> int:
        """Validate word count does not exceed 2500 words (FR-028)."""
        if v > 2500:
            raise ValueError("Job description exceeds 2500 words (~5 pages, FR-028)")
        return v

