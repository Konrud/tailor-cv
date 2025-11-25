# API Contracts

This directory contains the API contract specifications for the AI CV Tailor application.

## Files

- **`openapi.yaml`**: Complete OpenAPI 3.1.0 specification for all API endpoints

## API Overview

The AI CV Tailor API follows RESTful principles and provides endpoints for:

1. **CV Upload** (`/cv/*`): File upload, validation, and text extraction
2. **Job Description** (`/job/*`): Text input or URL extraction of job descriptions
3. **Analysis** (`/analyze`, `/tailor`): Gap analysis and CV tailoring
4. **Export** (`/export/*`): PDF and text download endpoints
5. **Health** (`/health`): Health check and API status

## Base URL

- **Development**: `http://localhost:8000/api/v1`
- **Production**: `https://api.tailorcv.example.com/api/v1`

## Authentication

No authentication required (session-only, stateless API per FR-017, FR-018).

## Request/Response Format

All endpoints use JSON for request/response bodies except:

- File uploads: `multipart/form-data`
- PDF downloads: `application/pdf`
- Text downloads: `text/plain`

## Error Handling

Standard HTTP status codes:

- `200`: Success
- `400`: Bad request (validation error)
- `404`: Resource not found
- `408`: Timeout (URL extraction)
- `410`: Gone (expired job posting)
- `413`: Payload too large (file >5MB)
- `422`: Unprocessable entity (Pydantic validation)
- `429`: Rate limit exceeded
- `500`: Internal server error
- `503`: Service unavailable (AI service down after retries)

Error responses follow the `ErrorResponse` schema defined in `openapi.yaml`.

## Typical Workflow

```
1. POST /cv/upload
   → Response: {id: cvId, ...}

2. POST /job/text OR /job/url
   → Response: {id: jobId, ...}

3. POST /analyze
   Body: {cvId, jobId}
   → Response: {id: gapAnalysisId, overallMatch, missingSkills, ...}

4. POST /tailor
   Body: {cvId, jobId, gapAnalysisId}
   → Response: {id: tailoredCvId, textVersion, pdfUrl, ...}

5. GET /export/pdf/{tailoredCvId}
   → Response: PDF file
```

## Generating TypeScript Types

To generate TypeScript interfaces from this OpenAPI spec, use [openapi-typescript](https://www.npmjs.com/package/openapi-typescript):

```bash
npx openapi-typescript openapi.yaml -o ../../../frontend/src/types/api.ts
```

## Viewing the Specification

### Online Viewers

1. **Swagger Editor**: https://editor.swagger.io/

   - Copy contents of `openapi.yaml` into the editor

2. **Redocly**: https://redocly.github.io/redoc/
   - Paste YAML URL or content

### Local Viewing

Using FastAPI's built-in documentation (when server is running):

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### CLI Tools

```bash
# Install swagger-cli
npm install -g @apidevtools/swagger-cli

# Validate spec
swagger-cli validate openapi.yaml

# Bundle spec (if using $ref references)
swagger-cli bundle openapi.yaml -o openapi-bundled.yaml
```

## Contract Validation

Ensure frontend TypeScript interfaces match backend Pydantic models by:

1. Generating TypeScript types from this OpenAPI spec
2. Validating API responses against these types during development
3. Reviewing API responses to ensure they match the expected schema

## Compliance with Feature Requirements

This API contract implements all functional requirements from `spec.md`:

- **FR-001 to FR-003**: CV upload and job description endpoints
- **FR-004**: Text extraction (implicit in CV upload response)
- **FR-005**: Job requirement extraction (JobRequirements schema)
- **FR-006, FR-007**: Gap analysis endpoint
- **FR-008, FR-009**: CV tailoring endpoint
- **FR-010 to FR-010b**: Anti-fabrication validation (validationPassed field)
- **FR-011, FR-012**: Text and PDF export endpoints
- **FR-013, FR-014**: Gap analysis and relevance in response schemas
- **FR-015 to FR-020**: Error handling, timeouts, retries
- **FR-021 to FR-028**: Validation rules enforced at API layer

## Versioning

This API follows semantic versioning (SemVer):

- **Major version** (v1): Breaking changes
- **Minor version**: New features (backward compatible)
- **Patch version**: Bug fixes

Current version: `v1.0.0`

## Support

For API issues or questions, refer to:

- Feature specification: `../spec.md`
- Data model: `../data-model.md`
- Research decisions: `../research.md`
