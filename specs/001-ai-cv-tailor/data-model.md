# Data Model: AI CV Tailor

**Feature**: `001-ai-cv-tailor`  
**Date**: 2025-11-25  
**Phase**: 1 - Data Model Design

## Overview

This document defines the data structures for the AI CV Tailor application. Since the application uses session-only storage (no database persistence per FR-017, FR-018), these models represent:

- **Frontend**: TypeScript interfaces for client-side state
- **Backend**: Pydantic models for API request/response validation
- **Session**: Browser SessionStorage schema

## Core Entities

### 1. MasterCV

The user's original uploaded CV.

#### Frontend TypeScript Interface

```typescript
interface MasterCV {
  id: string; // UUID generated client-side
  fileName: string; // Original file name
  fileType: "pdf" | "docx" | "txt";
  fileSize: number; // Bytes (max 5MB per FR-001)
  uploadedAt: string; // ISO 8601 timestamp
  extractedText: string; // Plain text extracted from file
  parsedSections: CVSection[]; // Structured sections
  language: "en"; // English only (FR-025)
  pageCount: number; // Must be ≤ 5 (FR-027)
}

interface CVSection {
  type: "summary" | "experience" | "education" | "skills" | "certifications" | "other";
  title: string; // Section heading
  content: string; // Section text
  items: string[]; // Bullet points or list items
}
```

#### Backend Pydantic Model

```python
from pydantic import BaseModel, Field, field_validator
from typing import Literal
from datetime import datetime
from uuid import UUID

class CVSection(BaseModel):
    type: Literal['summary', 'experience', 'education', 'skills', 'certifications', 'other']
    title: str = Field(..., max_length=200)
    content: str = Field(..., max_length=10000)
    items: list[str] = Field(default_factory=list)

class MasterCV(BaseModel):
    id: UUID
    file_name: str = Field(..., max_length=255)
    file_type: Literal['pdf', 'docx', 'txt']
    file_size: int = Field(..., le=5_242_880)  # 5 MB in bytes
    uploaded_at: datetime
    extracted_text: str = Field(..., min_length=10, max_length=100000)
    parsed_sections: list[CVSection]
    language: Literal['en']
    page_count: int = Field(..., le=5, ge=1)  # FR-027: max 5 pages

    @field_validator('file_size')
    @classmethod
    def validate_file_size(cls, v: int) -> int:
        if v > 5_242_880:  # 5 MB
            raise ValueError('File size exceeds 5 MB limit (FR-001a)')
        return v
```

**Validation Rules**:

- File size: ≤ 5 MB (FR-001a)
- Page count: ≤ 5 pages (FR-027)
- Language: English only (FR-025)
- Extracted text: Must contain at least 10 characters

**State Transitions**:

```
[Upload] → Validating → Extracting → Parsed → [Ready for Tailoring]
```

---

### 2. JobDescription

The target job requirements from text input or URL extraction.

#### Frontend TypeScript Interface

```typescript
interface JobDescription {
  id: string; // UUID generated client-side
  source: "text" | "url"; // Input method
  sourceUrl?: string; // If from URL (FR-003)
  rawText: string; // Original job description text
  extractedAt: string; // ISO 8601 timestamp
  requirements: JobRequirements; // Parsed requirements
  language: "en"; // English only (FR-026)
  wordCount: number; // Must be ≤ 2500 words (~5 pages, FR-028)
  platform?: "linkedin" | "indeed" | "glassdoor" | "other"; // If from URL
}

interface JobRequirements {
  title: string; // Job title
  company?: string; // Company name (if available)
  seniorityLevel?: string; // e.g., "Senior", "Mid-level", "Entry"
  skills: RequiredSkill[]; // Required and preferred skills
  responsibilities: string[]; // Key responsibilities
  qualifications: string[]; // Required qualifications
  keywords: string[]; // Important keywords for ATS
}

interface RequiredSkill {
  name: string; // Skill name
  category: "technical" | "soft" | "domain" | "tool" | "language";
  required: boolean; // Required vs. preferred
  yearsExperience?: number; // If specified
}
```

#### Backend Pydantic Model

```python
from typing import Optional

class RequiredSkill(BaseModel):
    name: str = Field(..., max_length=100)
    category: Literal['technical', 'soft', 'domain', 'tool', 'language']
    required: bool
    years_experience: Optional[int] = Field(None, ge=0, le=50)

class JobRequirements(BaseModel):
    title: str = Field(..., max_length=200)
    company: Optional[str] = Field(None, max_length=200)
    seniority_level: Optional[str] = Field(None, max_length=50)
    skills: list[RequiredSkill]
    responsibilities: list[str] = Field(..., max_length=50)  # Max 50 items
    qualifications: list[str] = Field(..., max_length=50)
    keywords: list[str] = Field(..., max_length=100)

class JobDescription(BaseModel):
    id: UUID
    source: Literal['text', 'url']
    source_url: Optional[str] = Field(None, max_length=2048)
    raw_text: str = Field(..., min_length=10, max_length=50000)
    extracted_at: datetime
    requirements: JobRequirements
    language: Literal['en']
    word_count: int = Field(..., le=2500, ge=1)  # FR-028: ~5 pages
    platform: Optional[Literal['linkedin', 'indeed', 'glassdoor', 'other']] = None

    @field_validator('word_count')
    @classmethod
    def validate_word_count(cls, v: int) -> int:
        if v > 2500:  # ~5 pages equivalent
            raise ValueError('Job description exceeds 5 pages equivalent (FR-028)')
        return v
```

**Validation Rules**:

- Word count: ≤ 2500 words (FR-028)
- Language: English only (FR-026)
- Raw text: Must contain at least 10 characters
- URL timeout: 10 seconds (FR-016a) - enforced at API layer

**State Transitions**:

```
[Input Text] → Validating → Parsing → [Ready]
[Input URL] → Fetching (10s timeout) → Extracting → Parsing → [Ready]
```

---

### 3. GapAnalysis

Identified gaps between the user's CV and job requirements.

#### Frontend TypeScript Interface

```typescript
interface GapAnalysis {
  id: string; // UUID
  cvId: string; // References MasterCV.id
  jobId: string; // References JobDescription.id
  createdAt: string; // ISO 8601 timestamp
  overallMatch: number; // Percentage match (0-100)
  matchedSkills: MatchedSkill[]; // Skills found in CV
  missingSkills: MissingSkill[]; // Skills not in CV (FR-006)
  relevantExperience: RelevantExperience[]; // Matching experiences (FR-007)
  warnings: Warning[]; // Low match warnings (FR-022, FR-023)
}

interface MatchedSkill {
  skillName: string;
  matchConfidence: number; // 0-100, how well it matches
  cvSource: string; // Where found in CV (quote)
  jobRequirement: string; // From job description
}

interface MissingSkill {
  skillName: string;
  importance: "required" | "preferred";
  category: string;
  suggestedAlternatives?: string[]; // Similar skills user has
}

interface RelevantExperience {
  cvSection: string; // Which CV section
  cvContent: string; // Relevant excerpt from CV
  jobResponsibility: string; // Which job responsibility it matches
  relevanceScore: number; // 0-100
}

interface Warning {
  type: "low_match" | "minimal_job_info" | "processing_time";
  severity: "info" | "warning" | "error";
  message: string;
  recommendation?: string;
}
```

#### Backend Pydantic Model

```python
class MatchedSkill(BaseModel):
    skill_name: str
    match_confidence: int = Field(..., ge=0, le=100)
    cv_source: str = Field(..., max_length=500)
    job_requirement: str = Field(..., max_length=500)

class MissingSkill(BaseModel):
    skill_name: str
    importance: Literal['required', 'preferred']
    category: str
    suggested_alternatives: list[str] = Field(default_factory=list)

class RelevantExperience(BaseModel):
    cv_section: str
    cv_content: str = Field(..., max_length=1000)
    job_responsibility: str = Field(..., max_length=500)
    relevance_score: int = Field(..., ge=0, le=100)

class Warning(BaseModel):
    type: Literal['low_match', 'minimal_job_info', 'processing_time']
    severity: Literal['info', 'warning', 'error']
    message: str
    recommendation: Optional[str] = None

class GapAnalysis(BaseModel):
    id: UUID
    cv_id: UUID
    job_id: UUID
    created_at: datetime
    overall_match: int = Field(..., ge=0, le=100)
    matched_skills: list[MatchedSkill]
    missing_skills: list[MissingSkill]  # FR-006
    relevant_experience: list[RelevantExperience]  # FR-007
    warnings: list[Warning]  # FR-022, FR-023

    @field_validator('overall_match')
    @classmethod
    def check_low_match(cls, v: int, values) -> int:
        # FR-022: Warn if match rate below 30%
        if v < 30:
            # Warning added in warnings list
            pass
        return v
```

**Validation Rules**:

- Overall match: 0-100 percentage
- Match confidence/relevance scores: 0-100
- If overall_match < 30%: Add warning (FR-022)

---

### 4. TailoredCV

The optimized CV generated for the specific job.

#### Frontend TypeScript Interface

```typescript
interface TailoredCV {
  id: string; // UUID
  cvId: string; // References MasterCV.id
  jobId: string; // References JobDescription.id
  gapAnalysisId: string; // References GapAnalysis.id
  createdAt: string; // ISO 8601 timestamp
  textVersion: string; // Clean text version (FR-011)
  pdfUrl: string; // Download URL for PDF (FR-012)
  modifications: Modification[]; // Changes made
  keywordMatches: KeywordMatch[]; // Keywords incorporated
  processingTime: number; // Seconds taken (target: <20s, SC-005)
  validationPassed: boolean; // Anti-fabrication check (FR-010b)
}

interface Modification {
  section: string; // Which CV section modified
  modificationType: "rewrite" | "reorder" | "emphasis";
  original: string; // Original content
  modified: string; // Modified content
  reason: string; // Why modified
}

interface KeywordMatch {
  keyword: string; // Keyword from job description
  incorporated: boolean; // Successfully added
  location: string; // Where in tailored CV
  naturalness: number; // 0-100, how naturally it fits
}
```

#### Backend Pydantic Model

```python
class Modification(BaseModel):
    section: str
    modification_type: Literal['rewrite', 'reorder', 'emphasis']
    original: str = Field(..., max_length=2000)
    modified: str = Field(..., max_length=2000)
    reason: str = Field(..., max_length=500)

class KeywordMatch(BaseModel):
    keyword: str
    incorporated: bool
    location: str
    naturalness: int = Field(..., ge=0, le=100)

class TailoredCV(BaseModel):
    id: UUID
    cv_id: UUID
    job_id: UUID
    gap_analysis_id: UUID
    created_at: datetime
    text_version: str = Field(..., min_length=10, max_length=100000)  # FR-011
    pdf_url: str  # FR-012
    modifications: list[Modification]
    keyword_matches: list[KeywordMatch]
    processing_time: float = Field(..., le=20.0)  # SC-005: <20 seconds
    validation_passed: bool  # FR-010b: anti-fabrication check

    @field_validator('validation_passed')
    @classmethod
    def must_pass_validation(cls, v: bool) -> bool:
        if not v:
            raise ValueError('Tailored CV failed anti-fabrication validation (FR-010b)')
        return v
```

**Validation Rules**:

- Processing time: ≤ 20 seconds (SC-005)
- Validation must pass: True (FR-010b)
- Text version: Non-empty
- PDF URL: Valid URL

**State Transitions**:

```
[Request] → Processing → Validating → Generating PDF → [Complete]
                      ↓
                 [Fabrication Detected] → Error
```

---

### 5. ProcessingSession

Client-side session state (stored in SessionStorage).

#### Frontend TypeScript Interface (Session State)

```typescript
interface ProcessingSession {
  sessionId: string; // UUID for this session
  startedAt: string; // ISO 8601 timestamp
  masterCV?: MasterCV; // Uploaded CV
  jobDescription?: JobDescription; // Job description
  gapAnalysis?: GapAnalysis; // Gap analysis result
  tailoredCV?: TailoredCV; // Tailored CV result
  currentStep: ProcessingStep; // Current workflow step
  errors: SessionError[]; // Any errors encountered
}

type ProcessingStep =
  | "upload_cv"
  | "input_job"
  | "analyzing"
  | "tailoring"
  | "complete"
  | "error";

interface SessionError {
  timestamp: string; // When error occurred
  step: ProcessingStep; // Which step failed
  errorType: string; // Error category
  message: string; // User-friendly message
  technicalDetails?: string; // For debugging
  retryable: boolean; // Can user retry?
}
```

**SessionStorage Schema**:

```typescript
// Stored as: sessionStorage.setItem('tailorCV_session', JSON.stringify(session))
{
  "sessionId": "uuid",
  "startedAt": "2025-11-25T10:00:00Z",
  "masterCV": { /* MasterCV object */ },
  "jobDescription": { /* JobDescription object */ },
  "currentStep": "analyzing",
  "errors": []
}
```

**Lifecycle**:

- Created: On first CV upload
- Updated: After each processing step
- Cleared: On browser/tab close (automatic per SessionStorage API)
- Manual clear: User can clear via UI button

---

## Entity Relationships

```
ProcessingSession (1)
    ├── has one MasterCV (1)
    ├── has one JobDescription (1)
    ├── has one GapAnalysis (0..1)
    └── has one TailoredCV (0..1)

GapAnalysis (1)
    ├── references MasterCV (1)
    └── references JobDescription (1)

TailoredCV (1)
    ├── references MasterCV (1)
    ├── references JobDescription (1)
    └── references GapAnalysis (1)
```

**Relationship Rules**:

- GapAnalysis cannot exist without MasterCV and JobDescription
- TailoredCV cannot exist without MasterCV, JobDescription, and GapAnalysis
- All relationships are in-memory only (no foreign keys, per FR-017/FR-018)

---

## Validation Summary

### File Upload Validation (FR-001, FR-001a, FR-001b)

- ✅ File size ≤ 5 MB
- ✅ File type: PDF (text-extractable), DOCX, TXT
- ✅ Page count ≤ 5 pages (FR-027)
- ✅ Language: English (FR-025)
- ✅ Extracted text: Minimum 10 characters

### Job Description Validation (FR-002, FR-003, FR-026, FR-028)

- ✅ Source: text or URL
- ✅ URL timeout: 10 seconds (FR-016a)
- ✅ Word count ≤ 2500 words (FR-028)
- ✅ Language: English (FR-026)
- ✅ Minimum content: 10 characters

### Processing Validation (FR-010a, FR-010b, FR-019, FR-020)

- ✅ Anti-fabrication check before returning result
- ✅ Retry logic: 3 attempts with exponential backoff
- ✅ Processing time: ≤ 20 seconds target (SC-005)
- ✅ Error handling: User-friendly messages

### Match Rate Warnings (FR-022, FR-023)

- ✅ Warning if overall_match < 30%
- ✅ Warning if job description has minimal information
- ✅ Processing time warning if approaching 20s limit

---

## Type Safety & Validation Strategy

### Frontend (TypeScript)

- All interfaces strictly typed
- Runtime validation at API boundaries using Zod (optional but recommended)
- TanStack Query type inference from API responses

### Backend (Pydantic)

- All models with field validators
- Automatic OpenAPI schema generation
- Request/response validation at FastAPI route level

### Contract Validation

- Ensure TypeScript interfaces match Pydantic models
- Use OpenAPI schema to generate TypeScript types (openapi-typescript tool)
- API responses validated against frontend expectations
