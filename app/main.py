"""
Healthcare Document Assistant API - Main Application

This module initializes and configures the FastAPI application for the
Healthcare Document Assistant. It sets up CORS middleware, routes, and
provides the main application instance.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.v1.routes import router
from configs.config import AppInfo


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application instance.
    
    Returns:
        FastAPI: Configured FastAPI application instance
    """
    # Load application configuration
    app_config = AppInfo()
    
    # Initialize FastAPI application
    application = FastAPI(
        title=app_config.PROJECT_NAME,
        version=app_config.VERSION,
        description=app_config.DESCRIPTION,
        openapi_url=f"{app_config.API_V1_STR}/openapi.json",
        docs_url=f"{app_config.API_V1_STR}/docs",
        redoc_url=f"{app_config.API_V1_STR}/redoc"
    )
    
    # Configure CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=app_config.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routes
    application.include_router(router, prefix=app_config.API_V1_STR)
    
    return application


# Create the main application instance
app = create_application()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )