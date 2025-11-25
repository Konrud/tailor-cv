# Research: AI CV Tailor

**Feature**: `001-ai-cv-tailor`  
**Date**: 2025-11-25  
**Phase**: 0 - Research & Architecture

## Technology Stack Decisions

### Frontend Stack

#### Decision: React 19.2.0 with TypeScript 5.9.3 and Vite

**Rationale**:

- React provides component-based architecture ideal for SPA (aligns with Constitution I)
- TypeScript adds type safety, reducing runtime errors and improving maintainability
- Vite offers fast HMR (Hot Module Replacement) and optimized production builds
- Component-scoped vanilla CSS provides styling without additional complexity (aligns with Constitution III: Minimal Dependencies)

**Alternatives Considered**:

- Vue.js: Rejected - team expertise and ecosystem favor React
- Next.js: Rejected - SSR not needed for this SPA use case, adds unnecessary complexity
- Create React App: Rejected - Vite provides faster builds and better DX

**Implementation Notes**:

- Vite automatically handles CSS bundling, code splitting, and tree-shaking
- CSS modules via `component.module.css` naming convention for scoped styles
- Each component folder structure: `ComponentName/ComponentName.tsx` + `ComponentName.css`

### Frontend Dependencies

#### Decision: React Router 7.9.6 for Navigation

**Rationale**:

- Industry-standard routing for React SPAs
- Declarative routing aligns with React patterns
- Built-in lazy loading support for code splitting
- Active maintenance and large community

**Alternatives Considered**:

- TanStack Router: Rejected - newer, less mature, adds learning curve
- Reach Router: Rejected - merged into React Router

#### Decision: TanStack Query (React Query) 5.90.10 for Data Fetching

**Rationale**:

- Automatic caching, background refetching, and stale data management
- Reduces boilerplate for API calls, loading states, and error handling
- Optimistic updates support
- DevTools for debugging API state

**Alternatives Considered**:

- Redux + RTK Query: Rejected - overkill for this use case, more complex setup
- SWR: Rejected - TanStack Query has more features and better TypeScript support
- Axios alone: Rejected - doesn't provide caching or state management

### Backend Stack

#### Decision: Python 3.13.3 with FastAPI 0.122.0

**Rationale**:

- FastAPI provides automatic API documentation (OpenAPI/Swagger)
- Built-in Pydantic integration for request/response validation
- Async support for handling concurrent CV processing requests
- Excellent performance (comparable to Node.js/Go)
- Type hints improve code quality and IDE support

**Alternatives Considered**:

- Flask: Rejected - lacks async support and modern API features
- Django: Rejected - too heavyweight, includes ORM/admin we don't need
- Express.js (Node): Rejected - Python chosen for AI/ML ecosystem

#### Decision: Pydantic 2.12.4 for Data Validation

**Rationale**:

- Native FastAPI integration
- Type-safe validation with clear error messages
- Automatic JSON schema generation
- Excellent performance (Rust core in v2)

#### Decision: OpenAI Agents SDK (openai-agents-python)

**Rationale**:

- Official OpenAI library for agentic workflows ([source](https://github.com/openai/openai-agents-python))
- Built-in tracing and debugging capabilities
- Function calling support for structured CV parsing
- Handles retry logic and error handling out of the box
- Provider-agnostic design (can switch LLM providers if needed)

**Alternatives Considered**:

- LangChain: Rejected - too heavyweight, complex abstraction layers
- Direct OpenAI API calls: Rejected - would need to implement retry logic, tracing, and agent patterns manually
- AutoGen: Rejected - focused on multi-agent collaboration, overkill for single-agent CV tailoring

**Implementation Notes**:

- Use `@function_tool` decorator for CV parsing and job description extraction
- Implement separate agents for:
  - CV text extraction
  - Job description parsing
  - Gap analysis
  - CV tailoring/rewriting
- Use structured outputs for consistent response formats

### File Processing

#### Decision: PyMuPDF (fitz) for PDF Text Extraction

**Rationale**:

- Fast and reliable text extraction from PDF files
- Handles most PDF formats including text-based (required per FR-001b)
- Low memory footprint
- Active maintenance

**Alternatives Considered**:

- pdfplumber: Rejected - slower for large documents
- PyPDF2: Rejected - less reliable text extraction
- Apache Tika: Rejected - requires Java, adds deployment complexity

#### Decision: python-docx for DOCX Processing

**Rationale**:

- Standard library for reading .docx files
- Reliable paragraph and text extraction
- Lightweight

**Alternatives Considered**:

- docx2txt: Rejected - less control over formatting
- mammoth: Rejected - focused on HTML conversion, not text extraction

### Language Detection

#### Decision: langdetect for Language Identification

**Rationale**:

- Fast and accurate for English detection (FR-025, FR-026)
- Lightweight dependency
- Based on Google's language detection library
- Confidence scores for validation

**Alternatives Considered**:

- fasttext: Rejected - requires large model files
- polyglot: Rejected - complex dependencies
- Manual heuristics: Rejected - unreliable

### PDF Generation

#### Decision: ReportLab or WeasyPrint for ATS-Compatible PDF Generation

**Rationale**:

- ReportLab: Programmatic PDF creation with precise control over layout
- WeasyPrint: HTML/CSS to PDF, easier for structured content
- Both support clean, parseable text layers (required for ATS compatibility per FR-012)

**Decision**: Start with WeasyPrint (HTML template approach)

- Easier to maintain and modify templates
- Better separation of content and presentation
- Can fall back to ReportLab if specific ATS issues arise

**Alternatives Considered**:

- wkhtmltopdf: Rejected - deprecated, requires external binary
- PyPDF2: Rejected - primarily for manipulation, not creation
- pdfkit: Rejected - wrapper around wkhtmltopdf

## Architecture Decisions

### Application Architecture: SPA with RESTful API

**Decision**: Single Page Application frontend communicating with stateless REST API backend

**Rationale**:

- Aligns with Constitution I (SPA requirement)
- Clear separation of concerns
- Frontend can be served via CDN (performance optimization)
- Backend can scale horizontally
- Session-based storage handled client-side (aligns with FR-017, FR-018)

**API Communication Pattern**:

```
Frontend (React SPA)
    ↓ HTTP/HTTPS
Backend (FastAPI)
    ↓ API calls
OpenAI Agents SDK
    ↓ LLM API
OpenAI API
```

### State Management: Component State + TanStack Query

**Decision**: Use React hooks for UI state, TanStack Query for server state

**Rationale**:

- No global state management needed (aligns with Constitution III: Minimal Dependencies)
- TanStack Query handles all server state (CVs, job descriptions, results)
- React Context for minimal cross-component state (e.g., upload progress)

**Alternatives Considered**:

- Redux: Rejected - unnecessary complexity for this use case
- Zustand: Rejected - server state already handled by TanStack Query
- Recoil: Rejected - minimal cross-component state doesn't justify additional library

### Session Storage Strategy

**Decision**: Browser SessionStorage API for CV data retention

**Rationale**:

- Meets FR-017 requirement (data only during active browser session)
- Automatically clears on tab/browser close
- Synchronous API, simpler than IndexedDB
- 5-10 MB storage limit sufficient for CVs (FR-001: 5 MB max)

**Alternatives Considered**:

- LocalStorage: Rejected - persists after browser close (violates FR-017)
- IndexedDB: Rejected - unnecessary complexity for simple key-value storage
- In-memory only: Rejected - lost on page refresh

### File Upload Strategy

**Decision**: Direct file upload to backend with client-side validation

**Rationale**:

- Client validates file size (FR-001: 5 MB), format (FR-001b), before upload
- Backend performs secondary validation for security
- No intermediate storage (S3, etc.) needed due to session-only requirement

**Flow**:

1. User selects file
2. Client validates: size ≤ 5 MB, format in [PDF, DOCX, TXT]
3. Client sends to `/api/upload-cv` endpoint
4. Backend validates format, extracts text, stores in session
5. Returns extracted text to client

### URL Extraction Strategy

**Decision**: Backend-side web scraping with timeout

**Rationale**:

- CORS restrictions prevent client-side fetching
- Backend can handle redirects and rate limiting
- 10-second timeout enforced (FR-016a)
- Platform-specific parsers for LinkedIn, Indeed, Glassdoor

**Implementation**:

- Use `httpx` (async HTTP client) for requests
- BeautifulSoup4 for HTML parsing
- Platform-specific CSS selectors for job description extraction
- Fallback to OpenGraph meta tags if specific selectors fail

**Alternatives Considered**:

- Headless browser (Playwright): Rejected - too heavyweight, slow
- Third-party API: Rejected - adds cost and external dependency
- Client-side proxy: Rejected - violates CORS policies, security concerns

### Error Handling Strategy

**Decision**: Layered error handling with user-friendly messages

**Backend Error Mapping**:

```python
HTTP 400 → Client validation errors (file size, format, language)
HTTP 408 → Timeout errors (URL fetch, AI processing)
HTTP 422 → Pydantic validation errors
HTTP 429 → Rate limiting
HTTP 500 → Unexpected errors (logged, generic message to user)
HTTP 503 → AI service unavailable (after retries)
```

**Frontend Error Handling**:

- TanStack Query error boundaries
- Toast notifications for errors (consider react-hot-toast)
- Inline validation messages for forms
- Fallback UI for failed requests (retry buttons per FR-019)

### Processing Flow Architecture

**Decision**: Synchronous request with async backend processing

**Flow**:

```
1. User uploads CV + provides job description
   ↓
2. Backend validates inputs (size, format, language)
   ↓
3. Backend extracts text from CV
   ↓
4. Backend sends to OpenAI Agents SDK:
   - Agent 1: Parse CV structure
   - Agent 2: Parse job requirements
   - Agent 3: Generate gap analysis
   - Agent 4: Tailor CV (with anti-fabrication constraints)
   ↓
5. Backend validates tailored content against original (FR-010b)
   ↓
6. Backend generates PDF from tailored content
   ↓
7. Return to frontend: tailored text + PDF download URL + gap analysis
```

**Rationale**:

- SC-005 requires 20-second response time (feasible with OpenAI API)
- No need for async job queue for this latency requirement
- Simpler architecture (aligns with Constitution IV: Justified Complexity)

**Alternatives Considered**:

- Async job queue (Celery + Redis): Rejected - unnecessary for 20-second target
- WebSocket streaming: Rejected - adds complexity, not required by spec
- Polling: Rejected - user can wait synchronously for 20 seconds

### Anti-Fabrication Validation

**Decision**: Multi-layer validation approach

**Layers**:

1. **AI Prompt Engineering** (FR-010a):
   - Explicit instructions: "Only rewrite existing content. Never invent experience, skills, or qualifications."
   - Structured output format enforcing source references
2. **Automated Validation** (FR-010b):

   - Extract all claims from tailored CV
   - Fuzzy match against original CV content
   - Flag any claim without 70%+ similarity to original content
   - Reject tailored CV if fabrication detected

3. **Diff Report** (bonus feature):
   - Show user side-by-side comparison
   - Highlight changes made by AI

**Implementation**:

```python
from difflib import SequenceMatcher

def validate_no_fabrication(original_cv: str, tailored_cv: str) -> bool:
    tailored_claims = extract_claims(tailored_cv)  # Parse bullet points
    for claim in tailored_claims:
        if not has_source_in_original(claim, original_cv, threshold=0.7):
            raise FabricationError(f"Claim '{claim}' not found in original CV")
    return True
```

## Performance Optimization Strategies

### Frontend Optimization

**Code Splitting**:

- React.lazy() for route-based code splitting
- Dynamic imports for heavy components (PDF viewer, rich text editor)
- Vite automatically chunks vendor code

**Asset Optimization**:

- Vite minifies CSS and JS in production
- Use Web Font optimization (font-display: swap)
- Compress images (if any UI assets)

**Target Metrics** (Constitution VI: Performance First):

- Initial load: < 2 seconds (SC-009)
- Lighthouse score: > 90
- First Contentful Paint: < 1.5s
- Time to Interactive: < 3s

### Backend Optimization

**Caching Strategy**:

- No server-side caching needed (session-only data per FR-017)
- Client-side caching via TanStack Query (stale-while-revalidate)

**Concurrent Processing**:

- FastAPI async endpoints for I/O operations
- ThreadPoolExecutor for CPU-bound tasks (PDF parsing)
- SC-010 target: 100 concurrent users

**Response Time Budget**:

```
File upload + validation: 1-2 seconds
Text extraction: 2-3 seconds
AI processing: 10-15 seconds (includes retries)
PDF generation: 1-2 seconds
Total: ~20 seconds (SC-005 target)
```

## Security Considerations

**File Upload Security**:

- Validate file magic numbers (not just extensions)
- Limit file size (FR-001: 5 MB)
- Sanitize file names
- No file storage on disk (process in memory only)

**API Security**:

- CORS configuration (whitelist frontend domain)
- Rate limiting (prevent abuse)
- Input validation (Pydantic models)
- No authentication needed (stateless, session-only per FR-017)

**Data Privacy** (FR-017, FR-018):

- No database/persistent storage
- No server-side session storage
- No logging of CV content
- SSL/TLS for API communication

## Development Workflow

**Environment Setup**:

```
Frontend: npm/yarn workspaces (or single package)
Backend: Python venv or uv (as per openai-agents-python docs)
```

**Development Tools**:

- ESLint + Prettier (frontend code quality)
- Ruff (Python linter, as used by openai-agents-python)
- TypeScript strict mode
- Pre-commit hooks for formatting

## Accessibility & Responsiveness

**Accessibility** (Constitution VII):

- Semantic HTML (main, section, article, nav)
- ARIA labels for file upload, progress indicators
- Keyboard navigation support
- Screen reader testing (NVDA/JAWS)
- Color contrast ratio: WCAG AA minimum (4.5:1)

**Responsive Design** (Constitution II):

- Mobile-first CSS
- Breakpoints: 320px, 768px, 1024px, 1440px
- Touch-friendly file upload (drag-and-drop)
- Responsive typography (fluid type scale)
- Test on: iPhone SE, iPad, Desktop (Chrome DevTools)

## Deployment Considerations

**Frontend Deployment**:

- Static build output (`vite build`)
- Can deploy to: Netlify, Vercel, Cloudflare Pages, or static hosting
- Environment variables for API endpoint URL

**Backend Deployment**:

- FastAPI via Uvicorn ASGI server
- Options: Render, Railway, DigitalOcean App Platform, AWS Fargate
- Environment variables: `OPENAI_API_KEY`
- No persistent storage required (simplifies deployment)

**CI/CD** (Constitution: Build & Deployment Standards):

- Separate dev/staging/prod builds
- No auto-deploy (manual approval)
- Environment-specific configs

## Open Questions / Risks

**Resolved in Clarifications**:

- ✅ Language support: English-only (FR-025, FR-026)
- ✅ File size limits: 5 MB (FR-001a)
- ✅ Document length: 5 pages max (FR-027, FR-028)
- ✅ AI failure handling: 3 retries with exponential backoff (FR-019)
- ✅ URL timeout: 10 seconds (FR-016a)

**Minimal Remaining Risks**:

- OpenAI API rate limits: Monitor usage, implement user feedback
- ATS PDF compatibility: Test with multiple ATS systems (Greenhouse, Lever, Workday)
- Special characters in CVs: Handle during text extraction phase

## References

- [OpenAI Agents SDK Documentation](https://github.com/openai/openai-agents-python)
- [FastAPI Best Practices](https://fastapi.tiangolo.com/tutorial/)
- [React + TypeScript Patterns](https://react-typescript-cheatsheet.netlify.app/)
- [TanStack Query v5 Docs](https://tanstack.com/query/latest)
- [Vite Guide](https://vitejs.dev/guide/)
- [WCAG 2.1 AA Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)
