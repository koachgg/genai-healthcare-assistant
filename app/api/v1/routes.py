"""
API v1 Routes

This module aggregates all API v1 endpoint routers and provides a unified
router for the FastAPI application.
"""

from fastapi import APIRouter

# Import endpoint routers
from api.v1.endpoints.get_presigned_url import router as presigned_url_router
from api.v1.endpoints.trigger_process_document import router as process_document_router
from api.v1.endpoints.get_processed_documents import router as processed_documents_router
from api.v1.endpoints.get_summary import router as summary_router
from api.v1.endpoints.get_images import router as images_router
from api.v1.endpoints.get_tables import router as tables_router
from api.v1.endpoints.get_preview import router as preview_router
from api.v1.endpoints.generate_content import router as content_generation_router
from api.v1.endpoints.content_findings import router as content_findings_router
from api.v1.endpoints.get_prompt_library import router as prompt_library_router
from api.v1.endpoints.create_workspace import router as workspace_router
from api.v1.endpoints.google_drive import router as google_drive_router


# Create main API router
router = APIRouter()


# Include all endpoint routers
router.include_router(presigned_url_router, tags=["S3 Storage"])
router.include_router(process_document_router, tags=["Document Processing"])
router.include_router(images_router, tags=["Document Images"])
router.include_router(processed_documents_router, tags=["Documents"])
router.include_router(summary_router, tags=["Document Analysis"])
router.include_router(tables_router, tags=["Document Tables"])
router.include_router(preview_router, tags=["Document Preview"])
router.include_router(content_generation_router, tags=["Content Generation"])
router.include_router(content_findings_router, tags=["Content Analysis"])
router.include_router(prompt_library_router, tags=["Prompt Library"])
router.include_router(workspace_router, tags=["Workspace Management"])
router.include_router(google_drive_router, tags=["Google Drive Integration"])


@router.get("/health", tags=["Health Check"])
async def health_check():
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        dict: Status information including HTTP status code, message, and version
    """
    return {
        "status": "healthy",
        "message": "Healthcare Document Assistant API is running successfully",
        "version": "1.0.0"
    }