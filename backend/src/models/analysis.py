"""Pydantic models for analysis and tailoring data structures.

This module defines models for gap analysis, CV tailoring, and related components.
"""

from datetime import datetime
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class Modification(BaseModel):
    """A single modification made to the CV during tailoring."""

    section: str = Field(..., max_length=200, description="Which CV section was modified")
    modification_type: Literal["rewrite", "reorder", "emphasis"] = Field(
        ..., description="Type of modification applied"
    )
    original: str = Field(..., max_length=2000, description="Original content")
    modified: str = Field(..., max_length=2000, description="Modified content")
    reason: str = Field(..., max_length=500, description="Explanation for the modification")


class KeywordMatch(BaseModel):
    """A keyword from job description incorporated into tailored CV."""

    keyword: str = Field(..., max_length=100, description="Keyword from job description")
    incorporated: bool = Field(..., description="Whether successfully added to CV")
    location: str = Field(..., max_length=200, description="Where in tailored CV")
    naturalness: int = Field(
        ..., ge=0, le=100, description="How naturally the keyword fits (0-100)"
    )


class TailoredCV(BaseModel):
    """Optimized CV generated for a specific job.

    This model represents the final output of the tailoring process,
    including validation status and modifications made.
    """

    id: UUID = Field(default_factory=uuid4)
    cv_id: UUID = Field(..., description="References MasterCV.id")
    job_id: UUID = Field(..., description="References JobDescription.id")
    gap_analysis_id: UUID = Field(..., description="References GapAnalysis.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    text_version: str = Field(
        ..., min_length=10, max_length=100000, description="Clean text version (FR-011)"
    )
    pdf_url: str = Field(..., description="Download URL for PDF (FR-012)")
    modifications: list[Modification] = Field(
        ..., description="Changes made during tailoring"
    )
    keyword_matches: list[KeywordMatch] = Field(
        ..., description="Keywords incorporated from job"
    )
    processing_time: float = Field(
        ..., le=20.0, description="Seconds taken (target: <20s per SC-005)"
    )
    validation_passed: bool = Field(
        ..., description="Anti-fabrication check result (FR-010b)"
    )

    @field_validator("validation_passed")
    @classmethod
    def must_pass_validation(cls, v: bool) -> bool:
        """Ensure tailored CV passed anti-fabrication validation (FR-010b)."""
        if not v:
            raise ValueError("Tailored CV failed anti-fabrication validation")
        return v


class MatchedSkill(BaseModel):
    """A skill found in both CV and job description."""

    skill_name: str = Field(..., max_length=100)
    match_confidence: int = Field(..., ge=0, le=100, description="Confidence of match (0-100)")
    cv_source: str = Field(..., max_length=500, description="Where found in CV")
    job_requirement: str = Field(..., max_length=500, description="From job description")


class MissingSkill(BaseModel):
    """A skill required by job but not found in CV."""

    skill_name: str = Field(..., max_length=100)
    importance: Literal["required", "preferred"] = Field(..., description="Skill importance")
    category: str = Field(..., max_length=50, description="Skill category")
    suggested_alternatives: list[str] = Field(
        default_factory=list, description="Similar skills user has"
    )


class RelevantExperience(BaseModel):
    """Experience from CV relevant to job requirements."""

    cv_section: str = Field(..., max_length=200, description="Which CV section")
    cv_content: str = Field(..., max_length=1000, description="Relevant CV excerpt")
    job_responsibility: str = Field(
        ..., max_length=500, description="Which job responsibility it matches"
    )
    relevance_score: int = Field(..., ge=0, le=100, description="Relevance score (0-100)")


class Warning(BaseModel):
    """Warning or notification for the user."""

    type: Literal["low_match", "minimal_job_info", "processing_time"] = Field(
        ..., description="Warning category"
    )
    severity: Literal["info", "warning", "error"] = Field(..., description="Severity level")
    message: str = Field(..., max_length=500, description="User-friendly message")
    recommendation: str | None = Field(None, max_length=500, description="Suggested action")


class GapAnalysis(BaseModel):
    """Analysis of gaps between CV and job requirements.

    This model identifies missing skills, matched skills, and relevant
    experience to help users understand their fit for the job.
    """

    id: UUID = Field(default_factory=uuid4)
    cv_id: UUID = Field(..., description="References MasterCV.id")
    job_id: UUID = Field(..., description="References JobDescription.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    overall_match: int = Field(..., ge=0, le=100, description="Overall match percentage (0-100)")
    matched_skills: list[MatchedSkill] = Field(..., description="Skills found in CV (FR-007)")
    missing_skills: list[MissingSkill] = Field(..., description="Skills not in CV (FR-006)")
    relevant_experience: list[RelevantExperience] = Field(
        ..., description="Matching experiences (FR-007)"
    )
    warnings: list[Warning] = Field(..., description="Warnings for user (FR-022, FR-023)")

    @field_validator("overall_match")
    @classmethod
    def check_low_match_warning(cls, v: int, info) -> int:
        """Add warning if match rate is below 30% (FR-022)."""
        # Warning will be added to warnings list in service layer
        return v

