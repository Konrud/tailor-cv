"""API endpoints for AI CV Tailor.

This module exports all API routers and provides the health check endpoint.
"""

from datetime import datetime

from fastapi import APIRouter

# Health check router
health_router = APIRouter()


@health_router.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint.

    Returns:
        dict: Health status information
    """
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
