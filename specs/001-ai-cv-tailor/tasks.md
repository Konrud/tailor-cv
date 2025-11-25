# Tasks: AI CV Tailor

**Feature Branch**: `001-ai-cv-tailor`  
**Generated**: 2025-11-25  
**Input**: Design documents from `/specs/001-ai-cv-tailor/`  
**Prerequisites**: plan.md, spec.md, data-model.md, research.md, contracts/openapi.yaml, quickstart.md

**Tests**: NOT requested in feature specification - tasks below do NOT include test implementation

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

This project uses web app structure:
- Backend: `backend/src/`
- Frontend: `frontend/src/`

## Phase Numbering Note

Implementation phases below (Phase 1-7) follow task execution order. These correspond to plan.md as follows:
- plan.md Phase 0 (Research) → Already complete (research.md)
- plan.md Phase 1 (Design) → Already complete (data-model.md, contracts/, quickstart.md)
- plan.md Phase 2 (Tasks) → This file
- tasks.md Phase 1-7 → Implementation execution phases

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create backend project structure at backend/src/ with api/, models/, services/, utils/ directories
- [ ] T002 Create frontend project structure at frontend/src/ with components/, pages/, services/, types/, utils/, styles/ directories
- [ ] T003 [P] Initialize backend Python 3.13.3 project with FastAPI dependencies in backend/requirements.txt
- [ ] T004 [P] Initialize frontend React 19.2.0 + TypeScript 5.9.3 project with Vite in frontend/package.json
- [ ] T005 [P] Configure backend linting (Ruff) in backend/pyproject.toml
- [ ] T006 [P] Configure frontend linting (ESLint) and formatting (Prettier) in frontend/.eslintrc.json
- [ ] T007 Create backend .env.example with OPENAI_API_KEY, CORS_ORIGINS, MAX_FILE_SIZE_MB configuration
- [ ] T008 Create frontend .env.example with VITE_API_URL configuration
- [ ] T009 [P] Setup TypeScript strict mode configuration in frontend/tsconfig.json
- [ ] T010 [P] Setup global CSS variables and resets in frontend/src/styles/global.css

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T011 Create FastAPI app entry point with CORS configuration in backend/src/main.py
- [ ] T012 [P] Create configuration loading utility with Pydantic Settings in backend/src/utils/config.py
- [ ] T013 [P] Create custom exception classes for validation, timeout, fabrication errors in backend/src/utils/errors.py
- [ ] T014 [P] Create base Pydantic models for CVSection in backend/src/models/cv.py
- [ ] T015 [P] Create base Pydantic models for RequiredSkill, JobRequirements in backend/src/models/job.py
- [ ] T016 Create health check endpoint GET /health in backend/src/api/__init__.py
- [ ] T017 [P] Create TanStack Query setup and API client configuration in frontend/src/services/api.ts
- [ ] T018 [P] Create TypeScript type definitions for session storage in frontend/src/types/session.ts
- [ ] T019 [P] Create SessionStorage utility functions in frontend/src/utils/session-storage.ts
- [ ] T020 [P] Create client-side validation helpers in frontend/src/utils/validation.ts
- [ ] T021 [P] Create React Router setup with routes in frontend/src/App.tsx
- [ ] T022 [P] Create common UI components: Button in frontend/src/components/common/Button/
- [ ] T023 [P] Create common UI components: ErrorMessage in frontend/src/components/common/ErrorMessage/
- [ ] T024 [P] Create common UI components: LoadingSpinner in frontend/src/components/common/LoadingSpinner/
- [ ] T025 [P] Create common UI components: ProgressBar in frontend/src/components/common/ProgressBar/

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Upload CV and Job Description for Basic Tailoring (Priority: P1) 🎯 MVP

**Goal**: Enable users to upload a CV, paste a job description, and receive a tailored CV with PDF download

**Independent Test**: Upload a sample PDF CV file and paste a job description text, verify the system produces a tailored CV output with relevant keywords and reorganized content, and can download both text and PDF versions

### Backend Implementation for User Story 1

- [ ] T026 [P] [US1] Implement file validation service (size ≤5MB, format check, page count ≤5 pages per FR-027) in backend/src/services/validator.py
- [ ] T027 [P] [US1] Implement PDF text extraction using PyMuPDF in backend/src/services/file_processor.py
- [ ] T028 [P] [US1] Implement DOCX text extraction using python-docx in backend/src/services/file_processor.py
- [ ] T029 [P] [US1] Implement language detection using langdetect in backend/src/services/language_detector.py
- [ ] T030 [US1] Create complete MasterCV Pydantic model with validation rules in backend/src/models/cv.py (depends on T014)
- [ ] T031 [US1] Create complete JobDescription Pydantic model with validation rules in backend/src/models/job.py (depends on T015)
- [ ] T032 [US1] Create Modification, KeywordMatch Pydantic models in backend/src/models/analysis.py
- [ ] T033 [US1] Create TailoredCV Pydantic model with anti-fabrication validation in backend/src/models/analysis.py
- [ ] T034 [US1] Implement POST /cv/upload endpoint with file extraction and validation in backend/src/api/cv.py (depends on T026-T029)
- [ ] T035 [US1] Implement POST /cv/validate endpoint for pre-flight validation in backend/src/api/cv.py
- [ ] T036 [US1] Implement POST /job/text endpoint with word count validation (≤2500 words per FR-028) and parsing logic in backend/src/api/job.py (depends on T029, T031)
- [ ] T037 [US1] Initialize OpenAI Agents SDK client in backend/src/services/ai_agent.py
- [ ] T038 [US1] Implement CV parsing agent with structured output in backend/src/services/ai_agent.py (depends on T037)
- [ ] T039 [US1] Implement job description parsing agent in backend/src/services/ai_agent.py (depends on T037)
- [ ] T040 [US1] Implement CV tailoring agent with anti-fabrication constraints (FR-010a) in backend/src/services/cv_tailor.py (depends on T037)
- [ ] T041 [US1] Implement anti-fabrication validation logic (FR-010b) in backend/src/services/validator.py (depends on T026)
- [ ] T042 [US1] Implement retry logic with exponential backoff (FR-019, FR-020) in backend/src/services/ai_agent.py
- [ ] T043 [US1] Implement POST /tailor endpoint with orchestration logic in backend/src/api/analysis.py (depends on T038-T042)
- [ ] T044 [US1] Implement ATS-compatible PDF generation using WeasyPrint in backend/src/services/pdf_generator.py
- [ ] T045 [US1] Implement GET /export/pdf/{tailoredCvId} endpoint in backend/src/api/export.py (depends on T044)
- [ ] T046 [US1] Implement GET /export/text/{tailoredCvId} endpoint in backend/src/api/export.py

### Frontend Implementation for User Story 1

- [ ] T047 [P] [US1] Generate TypeScript types from OpenAPI spec to frontend/src/types/api.ts
- [ ] T048 [P] [US1] Create CVUpload component with file dropzone and validation in frontend/src/components/CVUpload/CVUpload.tsx
- [ ] T049 [P] [US1] Style CVUpload component with responsive design in frontend/src/components/CVUpload/CVUpload.css
- [ ] T050 [P] [US1] Create JobInput component with text area for job description in frontend/src/components/JobInput/JobInput.tsx
- [ ] T051 [P] [US1] Style JobInput component with responsive design in frontend/src/components/JobInput/JobInput.css
- [ ] T052 [P] [US1] Create TailoredResult component with text preview and PDF download button in frontend/src/components/TailoredResult/TailoredResult.tsx
- [ ] T053 [P] [US1] Style TailoredResult component with responsive design in frontend/src/components/TailoredResult/TailoredResult.css
- [ ] T054 [US1] Create TanStack Query hook for CV upload (POST /cv/upload) in frontend/src/services/api.ts
- [ ] T055 [US1] Create TanStack Query hook for job text submission (POST /job/text) in frontend/src/services/api.ts
- [ ] T056 [US1] Create TanStack Query hook for CV tailoring (POST /tailor) in frontend/src/services/api.ts
- [ ] T057 [US1] Create Home page with landing content in frontend/src/pages/Home.tsx
- [ ] T058 [US1] Style Home page with responsive design in frontend/src/pages/Home.css
- [ ] T059 [US1] Create Upload page integrating CVUpload and JobInput components in frontend/src/pages/Upload.tsx
- [ ] T060 [US1] Create Results page integrating TailoredResult component in frontend/src/pages/Results.tsx
- [ ] T061 [US1] Implement session storage persistence for CV and job data in frontend/src/utils/session-storage.ts (depends on T019)
- [ ] T062 [US1] Add error handling with user-friendly messages for all API calls in frontend/src/services/api.ts
- [ ] T063 [US1] Add loading states and progress indicators to Upload page workflow in frontend/src/pages/Upload.tsx

**Checkpoint**: User Story 1 MVP complete - users can upload CV, paste job description, receive tailored CV with PDF download

---

## Phase 4: User Story 2 - Job URL Input for LinkedIn/External Job Postings (Priority: P2)

**Goal**: Enable users to provide a job posting URL instead of manual copy-paste

**Independent Test**: Provide a LinkedIn job URL, verify the system extracts the job description and generates a tailored CV without requiring manual text input

### Backend Implementation for User Story 2

- [ ] T064 [P] [US2] Implement URL validation and platform detection in backend/src/services/url_extractor.py
- [ ] T065 [P] [US2] Implement LinkedIn job description scraper using httpx and BeautifulSoup4 in backend/src/services/url_extractor.py
- [ ] T066 [P] [US2] Implement Indeed job description scraper in backend/src/services/url_extractor.py
- [ ] T067 [P] [US2] Implement Glassdoor job description scraper in backend/src/services/url_extractor.py
- [ ] T068 [US2] Implement generic scraper with OpenGraph meta tag fallback in backend/src/services/url_extractor.py (depends on T064-T067)
- [ ] T069 [US2] Implement 10-second timeout logic (FR-016a) in backend/src/services/url_extractor.py
- [ ] T070 [US2] Implement expired/removed posting detection (404/410 handling, FR-016b) in backend/src/services/url_extractor.py
- [ ] T071 [US2] Implement POST /job/url endpoint with URL extraction orchestration in backend/src/api/job.py (depends on T068-T070)

### Frontend Implementation for User Story 2

- [ ] T072 [P] [US2] Add URL input toggle to JobInput component in frontend/src/components/JobInput/JobInput.tsx
- [ ] T073 [P] [US2] Add URL validation logic to JobInput component in frontend/src/components/JobInput/JobInput.tsx
- [ ] T074 [US2] Create TanStack Query hook for job URL submission (POST /job/url) in frontend/src/services/api.ts
- [ ] T075 [US2] Add timeout error handling with fallback to manual paste in frontend/src/components/JobInput/JobInput.tsx
- [ ] T076 [US2] Update JobInput component styles for URL toggle in frontend/src/components/JobInput/JobInput.css

**Checkpoint**: User Story 2 complete - users can provide job URLs instead of manual text input

---

## Phase 5: User Story 3 - Gap Analysis and Relevance Highlighting (Priority: P2)

**Goal**: Provide users with insight into how well their CV matches the job requirements

**Independent Test**: Upload a CV with partial skill matches to a job description, verify the system identifies specific missing skills and highlights matching experiences with relevance scores

### Backend Implementation for User Story 3

- [ ] T077 [P] [US3] Create MatchedSkill, MissingSkill, RelevantExperience Pydantic models in backend/src/models/analysis.py
- [ ] T078 [P] [US3] Create Warning, GapAnalysis Pydantic models with validation in backend/src/models/analysis.py
- [ ] T079 [US3] Implement gap analysis agent with skill comparison logic in backend/src/services/gap_analyzer.py
- [ ] T080 [US3] Implement relevance scoring algorithm in backend/src/services/gap_analyzer.py
- [ ] T081 [US3] Implement low match rate detection (<30%, FR-022) in backend/src/services/gap_analyzer.py
- [ ] T082 [US3] Implement minimal job info detection (FR-023) in backend/src/services/gap_analyzer.py
- [ ] T083 [US3] Implement POST /analyze endpoint with gap analysis orchestration in backend/src/api/analysis.py (depends on T079-T082)
- [ ] T084 [US3] Update POST /tailor endpoint to require gapAnalysisId parameter in backend/src/api/analysis.py

### Frontend Implementation for User Story 3

- [ ] T085 [P] [US3] Create GapAnalysis component with skills grid display in frontend/src/components/GapAnalysis/GapAnalysis.tsx
- [ ] T086 [P] [US3] Add matched skills section to GapAnalysis component in frontend/src/components/GapAnalysis/GapAnalysis.tsx
- [ ] T087 [P] [US3] Add missing skills section with importance indicators to GapAnalysis component in frontend/src/components/GapAnalysis/GapAnalysis.tsx
- [ ] T088 [P] [US3] Add relevant experience section with relevance scores to GapAnalysis component in frontend/src/components/GapAnalysis/GapAnalysis.tsx
- [ ] T089 [P] [US3] Add warning display for low match rates to GapAnalysis component in frontend/src/components/GapAnalysis/GapAnalysis.tsx
- [ ] T090 [P] [US3] Style GapAnalysis component with responsive design in frontend/src/components/GapAnalysis/GapAnalysis.css
- [ ] T091 [US3] Create TanStack Query hook for gap analysis (POST /analyze) in frontend/src/services/api.ts
- [ ] T092 [US3] Update Upload page workflow to call /analyze before /tailor in frontend/src/pages/Upload.tsx
- [ ] T093 [US3] Integrate GapAnalysis component into Upload page workflow in frontend/src/pages/Upload.tsx
- [ ] T094 [US3] Add gap analysis data to session storage in frontend/src/utils/session-storage.ts

**Checkpoint**: User Story 3 complete - users see gap analysis with missing skills, matched skills, and relevance highlighting

---

## Phase 6: User Story 4 - CV Reorganization for Role-Specific Structure (Priority: P3)

**Goal**: Reorganize CV sections to emphasize most relevant experience first

**Independent Test**: Upload a CV with multiple work experiences and a job description emphasizing specific technologies, verify the tailored CV reorders sections to highlight matching experience first while maintaining chronological accuracy

### Backend Implementation for User Story 4

- [ ] T095 [US4] Implement section reordering logic in CV tailoring agent in backend/src/services/cv_tailor.py
- [ ] T096 [US4] Implement experience prioritization algorithm based on relevance scores in backend/src/services/cv_tailor.py
- [ ] T097 [US4] Implement skills section reordering to surface matching skills first in backend/src/services/cv_tailor.py
- [ ] T098 [US4] Add chronological accuracy validation to prevent date misrepresentation in backend/src/services/validator.py
- [ ] T099 [US4] Update TailoredCV model to track reordering modifications in backend/src/models/analysis.py

### Frontend Implementation for User Story 4

- [ ] T100 [P] [US4] Add modification history section to TailoredResult component in frontend/src/components/TailoredResult/TailoredResult.tsx
- [ ] T101 [P] [US4] Add side-by-side comparison view (original vs tailored) to TailoredResult component in frontend/src/components/TailoredResult/TailoredResult.tsx
- [ ] T102 [US4] Update TailoredResult component styles for comparison view in frontend/src/components/TailoredResult/TailoredResult.css

**Checkpoint**: User Story 4 complete - CVs are reorganized to emphasize most relevant experience while maintaining accuracy

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final production readiness

- [ ] T103 [P] Add comprehensive API documentation to OpenAPI spec in specs/001-ai-cv-tailor/contracts/openapi.yaml
- [ ] T104 [P] Add inline code comments for complex AI agent logic in backend/src/services/
- [ ] T105 [P] Add ARIA labels for accessibility to CVUpload component in frontend/src/components/CVUpload/CVUpload.tsx
- [ ] T106 [P] Add ARIA labels for accessibility to JobInput component in frontend/src/components/JobInput/JobInput.tsx
- [ ] T107 [P] Add ARIA labels for accessibility to GapAnalysis component in frontend/src/components/GapAnalysis/GapAnalysis.tsx
- [ ] T108 [P] Add ARIA labels for accessibility to TailoredResult component in frontend/src/components/TailoredResult/TailoredResult.tsx
- [ ] T109 [P] Implement keyboard navigation support across all components in frontend/src/components/
- [ ] T110 [P] Add color contrast validation for WCAG 2.1 AA compliance in frontend/src/styles/global.css
- [ ] T111 [P] Implement responsive breakpoints (320px, 768px, 1024px, 1440px) across all components in frontend/src/
- [ ] T112 Add rate limiting logic to prevent API abuse in backend/src/main.py
- [ ] T113 Add logging for processing times and error tracking in backend/src/services/
- [ ] T114 Add performance monitoring for 20-second processing target (SC-005) in backend/src/services/cv_tailor.py
- [ ] T114a [P] Add end-to-end workflow timing monitoring to track SC-001 target (<3 minutes) in backend/src/api/analysis.py
- [ ] T114b [P] Add extraction success rate logging to track SC-002 target (95%) in backend/src/services/file_processor.py
- [ ] T114c [P] Add LinkedIn extraction success rate logging to track SC-006 target (90%) in backend/src/services/url_extractor.py
- [ ] T115 Optimize frontend bundle size with lazy loading for heavy components in frontend/src/App.tsx
- [ ] T116 Add frontend error boundaries for graceful error handling in frontend/src/App.tsx
- [ ] T117 Create deployment guide documentation in docs/deployment.md
- [ ] T118 Create user guide documentation in docs/user-guide.md
- [ ] T119 Update README with project overview and quickstart instructions in README.md
- [ ] T120 Run quickstart.md validation to ensure all setup steps work correctly

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P2 → P3)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Extends JobInput component from US1, but independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Adds /analyze endpoint before /tailor, integrates with US1 workflow
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - Enhances CV tailoring logic from US1

### Within Each User Story

- Models before services
- Services before API endpoints
- Backend endpoints before frontend integration
- Core functionality before UI enhancements
- Story complete before moving to next priority

### Parallel Opportunities

- **Setup (Phase 1)**: T003-T004 (backend/frontend init), T005-T006 (linting), T009-T010 (config)
- **Foundational (Phase 2)**: T012-T015 (models/utils), T017-T020 (frontend utils), T022-T025 (common components)
- **User Story 1 Backend**: T026-T029 (file processing), T032-T033 (models), T045-T046 (export endpoints)
- **User Story 1 Frontend**: T047-T053 (component creation), T054-T056 (API hooks)
- **User Story 2 Backend**: T064-T067 (platform scrapers)
- **User Story 2 Frontend**: T072-T073 (JobInput enhancements)
- **User Story 3 Backend**: T077-T078 (models)
- **User Story 3 Frontend**: T085-T090 (GapAnalysis component sections)
- **User Story 4 Frontend**: T100-T101 (TailoredResult enhancements)
- **Polish (Phase 7)**: T103-T111 (documentation, accessibility, responsive design), T114a-T114c (monitoring)

---

## Parallel Example: User Story 1 Backend

```bash
# Launch all file processing services together:
Task: "Implement file validation service (size ≤5MB, format check) in backend/src/services/validator.py"
Task: "Implement PDF text extraction using PyMuPDF in backend/src/services/file_processor.py"
Task: "Implement DOCX text extraction using python-docx in backend/src/services/file_processor.py"
Task: "Implement language detection using langdetect in backend/src/services/language_detector.py"

# Launch all analysis models together:
Task: "Create Modification, KeywordMatch Pydantic models in backend/src/models/analysis.py"
Task: "Create TailoredCV Pydantic model with anti-fabrication validation in backend/src/models/analysis.py"

# Launch export endpoints together:
Task: "Implement GET /export/pdf/{tailoredCvId} endpoint in backend/src/api/export.py"
Task: "Implement GET /export/text/{tailoredCvId} endpoint in backend/src/api/export.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Backend → Frontend → Integration)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP! ✨)
3. Add User Story 2 → Test independently → Deploy/Demo (Enhanced input! 🚀)
4. Add User Story 3 → Test independently → Deploy/Demo (Gap insights! 📊)
5. Add User Story 4 → Test independently → Deploy/Demo (Smart reorganization! 🎯)
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Backend)
   - Developer B: User Story 1 (Frontend)
   - After US1 complete:
     - Developer A: User Story 2 + 3 (Backend)
     - Developer B: User Story 2 + 3 (Frontend)
     - Developer C: User Story 4
3. Stories complete and integrate independently

---

## Metrics

- **Total Tasks**: 123
- **Setup Tasks**: 10
- **Foundational Tasks**: 15
- **User Story 1 Tasks**: 38 (26 backend + 12 frontend)
- **User Story 2 Tasks**: 13 (8 backend + 5 frontend)
- **User Story 3 Tasks**: 18 (8 backend + 10 frontend)
- **User Story 4 Tasks**: 8 (5 backend + 3 frontend)
- **Polish Tasks**: 21

### Parallel Opportunities

- Phase 1: 7 tasks can run in parallel
- Phase 2: 14 tasks can run in parallel
- User Story 1: 12 backend + 6 frontend tasks can run in parallel
- User Story 2: 4 backend + 2 frontend tasks can run in parallel
- User Story 3: 7 frontend tasks can run in parallel
- User Story 4: 2 frontend tasks can run in parallel
- Polish: 14 tasks can run in parallel (added 3 monitoring tasks)

### Suggested MVP Scope

**Minimum Viable Product**: User Story 1 only (Tasks T001-T063)
- Core value: Upload CV + paste job → receive tailored CV with PDF download
- 53 tasks total (10 setup + 15 foundational + 28 US1 implementation)
- Estimated effort: 2-3 weeks for single developer
- Note: New requirements (FR-029, FR-030) added for special character handling

---

## Notes

- [P] tasks = different files/independent work, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Backend tasks generally complete before frontend integration
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Tests NOT included per feature specification - no test tasks generated

