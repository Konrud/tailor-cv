# Quickstart Guide: AI CV Tailor

**Feature**: `001-ai-cv-tailor`  
**Last Updated**: 2025-11-25

This guide will help you set up and start developing the AI CV Tailor application locally.

## Prerequisites

Before you begin, ensure you have the following installed:

### Required

- **Node.js**: v20+ (for frontend)
- **Python**: 3.13.3 (for backend)
- **Git**: For version control
- **OpenAI API Key**: Get from https://platform.openai.com/api-keys

### Recommended

- **VS Code** or your preferred IDE
- **Postman** or **Thunder Client** for API testing
- **uv** (Python package manager) - recommended by openai-agents-python library

---

## Project Setup

### 1. Clone Repository

```bash
git clone <repository-url>
cd tailorCV
git checkout 001-ai-cv-tailor
```

### 2. Backend Setup

#### Using uv (Recommended)

```bash
# Install uv if you haven't
curl -LsSf https://astral.sh/uv/install.sh | sh

# Navigate to backend directory
cd backend

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
uv pip install fastapi uvicorn pydantic python-multipart
uv pip install pymupdf python-docx langdetect httpx beautifulsoup4
uv pip install weasyprint pillow
uv pip install openai-agents
```

#### Using pip (Alternative)

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
```

#### Create requirements.txt

```txt
# Backend dependencies
fastapi==0.122.0
uvicorn[standard]==0.38.0
pydantic==2.12.4
python-multipart==0.0.20

# File processing
pymupdf==1.26.6
python-docx==1.2.0
langdetect==1.0.9

# HTTP & web scraping
httpx==0.28.1
beautifulsoup4==4.12.3

# PDF generation
weasyprint==66.0
pillow==12.0.0

# AI processing
openai-agents==0.6.1
```

#### Environment Variables

Create `.env` file in backend directory:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini  # or gpt-4o for better quality

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true  # Development only

# CORS (for frontend)
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173

# Processing Limits
MAX_FILE_SIZE_MB=5
MAX_PAGE_COUNT=5
MAX_WORD_COUNT=2500
URL_TIMEOUT_SECONDS=10

# Retry Configuration
MAX_RETRIES=3
RETRY_DELAY_SECONDS=1
RETRY_BACKOFF_FACTOR=2
```

#### Start Backend Server

```bash
# From backend directory
uvicorn src.main:app --reload --port 8000

# Server will be available at http://localhost:8000
# API docs at http://localhost:8000/docs
```

### 3. Frontend Setup

```bash
# From project root
cd frontend

# Install dependencies
npm install

# Or using yarn
yarn install

# Or using pnpm
pnpm install
```

#### Create .env.local

```env
# API Configuration
VITE_API_URL=http://localhost:8000/api/v1

# Feature Flags (optional)
VITE_ENABLE_DEBUG=true
VITE_ENABLE_TRACING=false
```

#### Start Frontend Development Server

```bash
# From frontend directory
npm run dev

# Or
yarn dev

# Frontend will be available at http://localhost:5173
```

---

## Project Structure

```
tailorCV/
├── backend/
│   ├── src/
│   │   ├── main.py              # FastAPI app entry point
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── cv.py            # CV upload endpoints
│   │   │   ├── job.py           # Job description endpoints
│   │   │   ├── analysis.py      # Analysis & tailoring endpoints
│   │   │   └── export.py        # PDF/text export endpoints
│   │   ├── models/
│   │   │   ├── __init__.py
│   │   │   ├── cv.py            # Pydantic models for CV
│   │   │   ├── job.py           # Pydantic models for job
│   │   │   └── analysis.py      # Pydantic models for analysis
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   ├── file_processor.py    # PDF/DOCX/TXT extraction
│   │   │   ├── language_detector.py # Language detection
│   │   │   ├── url_extractor.py     # Job URL extraction
│   │   │   ├── ai_agent.py          # OpenAI Agents integration
│   │   │   ├── gap_analyzer.py      # Gap analysis logic
│   │   │   ├── cv_tailor.py         # CV tailoring logic
│   │   │   ├── validator.py         # Anti-fabrication validation
│   │   │   └── pdf_generator.py     # PDF generation
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── errors.py        # Custom exceptions
│   │       └── config.py        # Configuration loading
│   ├── .env
│   ├── .env.example
│   ├── requirements.txt
│   └── pyproject.toml           # If using uv
│
├── frontend/
│   ├── src/
│   │   ├── main.tsx             # React app entry point
│   │   ├── App.tsx              # Root component
│   │   ├── components/
│   │   │   ├── CVUpload/
│   │   │   │   ├── CVUpload.tsx
│   │   │   │   └── CVUpload.css
│   │   │   ├── JobInput/
│   │   │   │   ├── JobInput.tsx
│   │   │   │   └── JobInput.css
│   │   │   ├── GapAnalysis/
│   │   │   │   ├── GapAnalysis.tsx
│   │   │   │   └── GapAnalysis.css
│   │   │   ├── TailoredResult/
│   │   │   │   ├── TailoredResult.tsx
│   │   │   │   └── TailoredResult.css
│   │   │   └── common/          # Reusable UI components
│   │   ├── pages/
│   │   │   ├── Home.tsx
│   │   │   ├── Home.css
│   │   │   └── (other pages)
│   │   ├── services/
│   │   │   └── api.ts           # TanStack Query hooks
│   │   ├── types/
│   │   │   ├── api.ts           # Generated from OpenAPI
│   │   │   └── session.ts       # SessionStorage types
│   │   ├── utils/
│   │   │   ├── session-storage.ts
│   │   │   └── validation.ts
│   │   └── styles/
│   │       └── global.css       # Global styles
│   ├── public/
│   ├── .env.local
│   ├── .env.example
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── index.html
│
└── specs/
    └── 001-ai-cv-tailor/
        ├── spec.md              # Feature specification
        ├── plan.md              # This implementation plan
        ├── research.md          # Technology research
        ├── data-model.md        # Data structures
        ├── quickstart.md        # This file
        └── contracts/
            ├── openapi.yaml     # API specification
            └── README.md
```

---

## Development Workflow

### 1. Start Development Servers

```bash
# Terminal 1: Backend
cd backend
source .venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn src.main:app --reload --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

### 2. Verify Setup

**Backend Health Check:**

```bash
curl http://localhost:8000/api/v1/health
```

Expected response:

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-11-25T10:00:00Z"
}
```

**Frontend:**

Open http://localhost:5173 in your browser. You should see the AI CV Tailor landing page.

### 3. Test API Endpoints

#### Upload CV

```bash
curl -X POST http://localhost:8000/api/v1/cv/upload \
  -F "file=@/path/to/sample_cv.pdf"
```

#### Submit Job Description

```bash
curl -X POST http://localhost:8000/api/v1/job/text \
  -H "Content-Type: application/json" \
  -d '{
    "text": "We are seeking a Senior Software Engineer with 5+ years of Python experience..."
  }'
```

### 4. View API Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## Common Development Tasks

### Generate TypeScript Types from OpenAPI Spec

```bash
# From project root
npx openapi-typescript specs/001-ai-cv-tailor/contracts/openapi.yaml \
  -o frontend/src/types/api.ts
```

### Format Code

**Backend (Ruff):**

```bash
cd backend
ruff check src/ --fix
ruff format src/
```

**Frontend (Prettier):**

```bash
cd frontend
npm run format
```

### Lint Code

**Backend:**

```bash
cd backend
ruff check src/
mypy src/
```

**Frontend:**

```bash
cd frontend
npm run lint
```

### Build for Production

**Backend:**

```bash
# No build step needed for Python
# Just ensure all dependencies are in requirements.txt
```

**Frontend:**

```bash
cd frontend
npm run build

# Output in frontend/dist/
```

---

## Troubleshooting

### Backend Issues

**Issue**: `ModuleNotFoundError: No module named 'openai_agents'`

**Solution**:

```bash
pip install openai-agents
# or
uv pip install openai-agents
```

**Issue**: `OpenAI API rate limit exceeded`

**Solution**:

- Check your API key has sufficient quota
- Implement request throttling
- Use gpt-4o-mini instead of gpt-4o for development

**Issue**: PDF generation fails

**Solution**:

```bash
# WeasyPrint may need system dependencies
# On macOS:
brew install cairo pango gdk-pixbuf libffi

# On Ubuntu/Debian:
sudo apt-get install libcairo2 libpango-1.0 libpangocairo-1.0 libgdk-pixbuf2.0
```

### Frontend Issues

**Issue**: CORS errors when calling API

**Solution**: Ensure `CORS_ORIGINS` in backend `.env` includes your frontend URL (`http://localhost:5173`).

**Issue**: TypeScript errors after API changes

**Solution**: Regenerate types from OpenAPI spec:

```bash
npx openapi-typescript specs/001-ai-cv-tailor/contracts/openapi.yaml \
  -o frontend/src/types/api.ts
```

**Issue**: SessionStorage not persisting

**Solution**: Check browser privacy settings. SessionStorage should work by default, but some privacy extensions may block it.

---

## Next Steps

1. **Read the Feature Spec**: `specs/001-ai-cv-tailor/spec.md`
2. **Review Data Model**: `specs/001-ai-cv-tailor/data-model.md`
3. **Check API Contracts**: `specs/001-ai-cv-tailor/contracts/openapi.yaml`
4. **Read Technology Research**: `specs/001-ai-cv-tailor/research.md`
5. **Start Building**: Implement endpoints and components based on the plan

## Resources

- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React + TypeScript Cheatsheet](https://react-typescript-cheatsheet.netlify.app/)
- [TanStack Query Docs](https://tanstack.com/query/latest)
- [Vite Guide](https://vitejs.dev/guide/)

## Support

For questions or issues:

1. Check the specification documents in `specs/001-ai-cv-tailor/`
2. Review the implementation plan (`plan.md`)
3. Consult the research decisions (`research.md`)
