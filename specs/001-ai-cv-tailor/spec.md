# Feature Specification: AI CV Tailor

**Feature Branch**: `001-ai-cv-tailor`  
**Created**: 2025-11-25  
**Status**: Draft  
**Input**: User description: "tailor cv application AI resume optimizer. Users upload their master CV, paste a job description or URL, and receive a tailored version that matches required keywords, phrasing and structure. The user provides their original CV plus the job description they want to target or url (e.g. linkedin). The system extracts the employer's required skills, terminology, seniority level and responsibilities. It identifies gaps and key relevance points. The AI rewrites and reorganizes the CV to emphasize matching experience. It reframes bullet points, adds necessary keywords naturally, and keeps everything truthful and consistent with the user's real background. The user receives a clean text version and a downloadable PDF ready for the ATS."

## Clarifications

### Session 2025-11-25

- Q: What happens when the AI service fails, times out, or returns errors during CV tailoring? → A: Automatically retry up to 3 times with exponential backoff, then fail with error message
- Q: What is the maximum file size limit for CV uploads? → A: 5 MB max
- Q: How long should the system wait before timing out when fetching job descriptions from URLs? → A: 10 seconds timeout
- Q: How should the system handle unsupported file formats (images, scanned PDFs)? → A: Reject images and scanned PDFs immediately with message to use text-based formats (PDF, DOCX, TXT)
- Q: What occurs when a user's CV has no overlap with job requirements? → A: Generate best-effort tailored CV with prominent warning about low match rate and limited optimization
- Q: How does the system handle job descriptions with minimal information or vague requirements? → A: Process with warning that minimal job information may result in limited tailoring quality
- Q: What occurs when the user uploads a CV in a language different from the job description? → A: English-only - detect language and reject non-English CVs or job descriptions with helpful error message
- Q: How does the system handle very long CVs (10+ pages) or job descriptions? → A: Reject CVs or job descriptions exceeding 5 pages with error message to reduce content
- Q: What happens when a URL points to an expired or removed job posting? → A: Detect expired/removed postings (404/410 errors) and provide option to manually paste job description text instead
- Q: How does the system ensure CV tailoring remains truthful and doesn't fabricate experience? → A: AI instruction constraints forbidding fabrication + automated validation that all tailored content has basis in original CV

## User Scenarios & Testing _(mandatory)_

### User Story 1 - Upload CV and Job Description for Basic Tailoring (Priority: P1)

A job seeker uploads their master CV and pastes a job description from a job posting. The system analyzes both documents and generates a tailored CV that emphasizes relevant experience and includes matching keywords while maintaining truthfulness.

**Why this priority**: This is the core value proposition of the application - the minimum viable feature that delivers immediate value to users seeking to optimize their CV for a specific role.

**Independent Test**: Can be fully tested by uploading a sample CV file and pasting a job description text, then verifying the system produces a tailored CV output that includes relevant keywords from the job description and reorganized content that matches the job requirements.

**Acceptance Scenarios**:

1. **Given** a user has a master CV file and job description text, **When** they upload the CV and paste the job description, **Then** the system extracts skills, terminology, seniority level, and responsibilities from the job description
2. **Given** the job analysis is complete, **When** the system processes the CV, **Then** it produces a tailored version that emphasizes matching experience and naturally incorporates relevant keywords
3. **Given** a tailored CV has been generated, **When** the user views the output, **Then** they see a clean text version and can download a PDF formatted for ATS systems

---

### User Story 2 - Job URL Input for LinkedIn/External Job Postings (Priority: P2)

A user provides a LinkedIn or external job posting URL instead of copying/pasting the description. The system automatically extracts the job details from the URL and proceeds with CV tailoring.

**Why this priority**: This enhances user experience by removing the manual copy-paste step, making the workflow more seamless for users who find jobs on LinkedIn or other platforms.

**Independent Test**: Can be tested independently by providing a LinkedIn job URL and verifying the system extracts the job description and generates a tailored CV without requiring manual text input.

**Acceptance Scenarios**:

1. **Given** a user has a job posting URL, **When** they enter the URL instead of pasting text, **Then** the system fetches and extracts the job description from the URL within 10 seconds
2. **Given** the URL is from a supported platform (LinkedIn, Indeed, etc.), **When** extraction is attempted, **Then** the system successfully parses skills, requirements, and responsibilities
3. **Given** URL extraction fails or times out after 10 seconds, **When** an error occurs, **Then** the user receives a clear message and option to paste text manually instead

---

### User Story 3 - Gap Analysis and Relevance Highlighting (Priority: P2)

After analyzing the job description and CV, the system identifies gaps between the user's experience and job requirements, and highlights key relevance points that match.

**Why this priority**: This provides users with insight into how well their background matches the role and helps them understand what the AI emphasized or couldn't address.

**Independent Test**: Can be tested by providing a CV with partial matches to a job description and verifying the system identifies specific gaps (missing skills) and relevance points (matching experience).

**Acceptance Scenarios**:

1. **Given** a job description with specific required skills, **When** some skills are missing from the CV, **Then** the system identifies and lists these gaps for the user
2. **Given** the user's CV contains relevant experience, **When** the analysis is complete, **Then** the system highlights which experiences best match the job requirements
3. **Given** gap and relevance analysis is shown, **When** the user reviews it, **Then** they understand which parts of their CV were emphasized and what requirements couldn't be addressed

---

### User Story 4 - CV Reorganization for Role-Specific Structure (Priority: P3)

The system reorganizes CV sections (e.g., moving most relevant experience to the top, reordering skills) to match the structure and priorities evident in the job description.

**Why this priority**: This is an advanced feature that provides additional optimization beyond keyword matching, helping CVs pass both ATS systems and human reviewers.

**Independent Test**: Can be tested by providing a CV with multiple experiences and a job description emphasizing specific role types, then verifying the output CV reorders content to highlight the most relevant sections first.

**Acceptance Scenarios**:

1. **Given** a CV with multiple work experiences, **When** a job emphasizes specific experience types, **Then** the tailored CV places the most relevant experience in prominent positions
2. **Given** a job description highlights specific technical skills, **When** the CV is reorganized, **Then** matching skills appear earlier in the skills section
3. **Given** reorganization is applied, **When** the user compares original and tailored versions, **Then** the changes maintain chronological accuracy while emphasizing relevance

---

### Edge Cases

- Image files and scanned PDFs are rejected immediately with guidance to use text-based formats (see FR-001b)
- CV uploads exceeding 5 MB are rejected with error message (see FR-001, FR-001a)
- Job descriptions with minimal information handled per FR-023, FR-024
- Low or no CV-job overlap results in best-effort tailored CV with prominent warning about limited optimization (see FR-021, FR-022)
- Truthfulness enforced via AI prompt constraints and automated validation that all tailored content has basis in original CV (see FR-010a, FR-010b)
- Expired or removed job posting URLs (404/410 errors) are detected with option to manually paste job description (see FR-016b)
- CVs exceeding 5 pages and job descriptions exceeding 5 pages equivalent are rejected with error message (see FR-027, FR-028)
- Non-English CVs and job descriptions are detected and rejected with error message (English-only support) (see FR-025, FR-026)
- Special characters (Unicode, accents, symbols) are preserved during text extraction; non-standard formatting (tables, columns, text boxes) may be flattened to plain text with best-effort structure preservation; creative layouts (infographics, charts) not supported - reject with error message if text extraction confidence is low
- AI API failures are handled with 3 automatic retries using exponential backoff before showing error (see FR-019, FR-020)

## Requirements _(mandatory)_

### Functional Requirements

- **FR-001**: System MUST accept CV uploads in common text-based formats (PDF with extractable text, DOCX, TXT) up to 5 MB in file size
- **FR-001a**: System MUST reject CV uploads exceeding 5 MB with a clear error message instructing users to reduce file size
- **FR-001b**: System MUST validate uploaded files are text-extractable and reject image files (JPG, PNG, GIF) and scanned PDFs with a clear message instructing users to convert to text-based format
- **FR-002**: System MUST accept job descriptions via text input (paste)
- **FR-003**: System MUST accept job descriptions via URL input for supported platforms (LinkedIn, Indeed, Glassdoor at minimum)
- **FR-004**: System MUST extract and parse text content from uploaded CV files
- **FR-005**: System MUST extract job requirements including skills, terminology, seniority level, and key responsibilities from job descriptions
- **FR-006**: System MUST identify gaps between user's CV content and job requirements
- **FR-007**: System MUST identify relevance points where user's experience matches job requirements
- **FR-008**: System MUST rewrite CV bullet points to incorporate relevant keywords naturally (keyword density ≤5%, AI naturalness score ≥70/100, keywords integrated into existing context rather than appended)
- **FR-009**: System MUST reorganize CV sections to emphasize matching experience (most relevant experience positioned in top 50% of CV, matching skills listed before non-matching skills, relevance score ≥70/100 prioritized)
- **FR-010**: System MUST maintain factual accuracy and consistency with the user's original background (no fabrication)
- **FR-010a**: System MUST include explicit anti-fabrication constraints in AI prompts instructing the AI to only rewrite/reorganize existing content, never invent experience, skills, or qualifications
- **FR-010b**: System MUST implement automated validation checks that verify all content in the tailored CV has corresponding source material in the original CV
- **FR-011**: System MUST generate a clean text version of the tailored CV
- **FR-012**: System MUST generate a downloadable PDF version formatted for ATS compatibility
- **FR-013**: System MUST display gap analysis to users showing missing requirements
- **FR-014**: System MUST display relevance highlights showing matching strengths
- **FR-015**: System MUST handle extraction failures gracefully with user-friendly error messages
- **FR-016**: System MUST validate that URLs point to actual job postings before processing and handle invalid URLs gracefully with user-friendly error messages, including:
  - **FR-016a**: Timeout URL extraction requests after 10 seconds and provide option to manually paste text instead
  - **FR-016b**: Detect expired or removed job postings (HTTP 404, 410 status) and provide option to manually paste text instead
- **FR-017**: System MUST preserve user privacy by storing CV data only during the active browser session and discarding all data when the user closes the tab or browser
- **FR-018**: System MUST NOT persist CV data beyond the current browser session (no server-side storage, database persistence, or cookies with CV content)
- **FR-019**: System MUST implement retry logic for AI API calls: automatically retry up to 3 times with exponential backoff when API calls fail or timeout
- **FR-020**: System MUST display a clear error message to users when AI processing fails after all retry attempts are exhausted
- **FR-021**: System MUST generate a tailored CV even when there is minimal or no overlap between the user's CV and job requirements
- **FR-022**: System MUST display a prominent warning message when CV-job match rate is low (below 30% keyword overlap), informing users that optimization is limited
- **FR-023**: System MUST detect when job descriptions contain minimal or vague information (<50 words, <3 identified skills, or no clear responsibilities) and display a warning that tailoring quality may be limited
- **FR-024**: System MUST process job descriptions with minimal information and generate tailored CVs using available data, focusing on general best practices when specific requirements are unclear
- **FR-025**: System MUST detect the language of uploaded CVs and reject non-English CVs with a clear error message
- **FR-026**: System MUST detect the language of job descriptions (text or extracted from URL) and reject non-English job descriptions with a clear error message
- **FR-027**: System MUST detect the page count of uploaded CVs and reject those exceeding 5 pages with a clear error message instructing users to condense content
- **FR-028**: System MUST detect the length of job descriptions and reject those exceeding 5 pages equivalent (approximately 2500 words) with a clear error message
- **FR-029**: System MUST handle common special characters (Unicode, accents, currency symbols, mathematical symbols) during CV text extraction and preserve them in tailored output
- **FR-030**: System MUST detect when CV uses non-extractable formatting (heavy graphics, complex layouts) and reject with error message: "Your CV contains complex formatting that cannot be processed. Please upload a text-based CV with standard formatting."

### Assumptions

- CV data will be stored client-side only (browser session storage) with no server-side persistence
- Users accept the trade-off that closing the browser requires re-uploading their CV
- Session-based storage provides sufficient privacy protection for sensitive CV data
- The application operates as a single-page application (SPA) per constitution requirements
- AI processing will be performed via API calls to an AI service without storing CV content on servers
- Standard ATS systems can parse PDF files with clean, structured formatting
- The application supports English language only for both CVs and job descriptions (MVP scope)

### Key Entities _(include if feature involves data)_

- **Master CV**: The user's original complete CV containing all their experience, skills, education, and accomplishments. Attributes include text content, format type, upload timestamp, and parsed sections (experience, skills, education)
- **Job Description**: The target job requirements extracted from text or URL. Attributes include source (manual text or URL), extracted skills, required experience level, key responsibilities, company information, and industry terminology
- **Tailored CV**: The optimized CV generated for the specific job. Attributes include original CV reference, target job reference, modifications applied, keyword matches, reorganization changes, and generation timestamp
- **Gap Analysis**: Identified mismatches between CV and job requirements. Attributes include missing skills, experience gaps, terminology differences, and suggested improvements
- **Relevance Mapping**: Connections between CV content and job requirements. Attributes include matched skills, relevant experiences, keyword alignment scores, and confidence ratings

## Success Criteria _(mandatory)_

### Measurable Outcomes

- **SC-001**: Users can complete the entire CV tailoring workflow (upload CV, input job, receive tailored output) in under 3 minutes
- **SC-002**: The system successfully extracts keywords and requirements from 95% of provided job descriptions
- **SC-003**: Generated tailored CVs include at least 80% of required keywords from the job description (defined as skills marked "required" and keywords mentioned ≥2 times) that are factually supported by the user's original CV
- **SC-004**: 90% of generated PDFs successfully pass standard ATS parsers (Greenhouse, Lever, Workday, and iCIMS) without formatting errors when tested with sample CVs
- **SC-005**: The system processes CV and job description pairs and generates output within 20 seconds for documents up to 5 pages
- **SC-006**: URL-based job description extraction succeeds for 90% of LinkedIn job postings
- **SC-007**: _(Post-MVP)_ Users rate the relevance and quality of tailored CVs at 4 out of 5 or higher in feedback surveys (feedback collection mechanism to be added post-launch)
- **SC-008**: Zero instances of fabricated experience or skills in tailored CVs (100% factual accuracy maintained)
- **SC-009**: The application loads and is interactive within 2 seconds on standard broadband connections
- **SC-010**: The system handles concurrent requests from 100 users without performance degradation
