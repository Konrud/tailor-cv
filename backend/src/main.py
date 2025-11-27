"""AI CV Tailor - FastAPI Application Entry Point.

This module initializes the FastAPI application with CORS configuration,
middleware, and API routes.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.api import health_router
from src.utils.config import settings
from src.utils.errors import CVTailorError


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan manager for startup/shutdown events."""
    # Startup
    print("🚀 AI CV Tailor API starting...")
    print(f"📝 OpenAI Model: {settings.openai_model}")
    print(f"🌐 CORS Origins: {settings.cors_origins_list}")

    yield

    # Shutdown
    print("👋 AI CV Tailor API shutting down...")


# Initialize FastAPI application
app = FastAPI(
    title="AI CV Tailor API",
    description="AI-powered CV tailoring for job applications",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handler for custom errors
@app.exception_handler(CVTailorError)
async def cv_tailor_error_handler(request, exc: CVTailorError) -> JSONResponse:
    """Handle custom CVTailorError exceptions with user-friendly messages."""
    return JSONResponse(
        status_code=400,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "details": exc.details,
        },
    )


# Include API routers
app.include_router(health_router, prefix="/api/v1", tags=["health"])


# Root endpoint
@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint - API information."""
    return {
        "name": "AI CV Tailor API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health",
    }

