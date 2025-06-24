from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from utils.error_handlers import (
    AppException,
    app_exception_handler,
    http_exception_handler,
    general_exception_handler
)
from utils.logger import logger
from config import settings
from database import init_db
import uvicorn
import os

# TODO: Need to add better error messages for common failures
# TODO: Rate limiting needs improvement - current implementation is basic
# TODO: Add more comprehensive logging for debugging

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="A modern banking system with credit scoring and financial management",
    version=settings.APP_VERSION,
    docs_url=None,  # Disable default docs
    redoc_url=None  # Disable default redoc
)

# Add CORS middleware
# Note: In production, we should restrict this to specific origins
# Current setup allows all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=settings.CORS_METHODS,
    allow_headers=settings.CORS_HEADERS,
)

# Add exception handlers
# These were added after spending hours debugging error responses
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)

# Custom OpenAPI schema
# Had to customize this to add proper security schemes
# The default one wasn't showing our JWT auth properly
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    
    openapi_schema = get_openapi(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="A modern banking system with credit scoring and financial management",
        routes=app.routes,
    )
    
    # Add security schemes
    # This took a while to get right - JWT docs weren't very clear
    openapi_schema["components"]["securitySchemes"] = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

# Custom docs endpoint
# Swagger UI was too basic, had to customize it
@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url="/openapi.json",
        title=f"{settings.APP_NAME} - API Documentation",
        swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui-bundle.js",
        swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui.css",
    )

# Health check endpoint
# Added this after deployment issues - helps monitor if the service is up
@app.get("/health")
async def health_check():
    logger.info("Health check requested")
    return {"status": "healthy"}

# Initialize database
# This was a pain to get right - connection pooling was tricky
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up application...")
    init_db()
    logger.info("Application startup complete")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down application...")

if __name__ == "__main__":
    logger.info(f"Starting {settings.APP_NAME} in {settings.ENVIRONMENT} mode")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=settings.DEBUG,
        ssl_keyfile=settings.SSL_KEYFILE,
        ssl_certfile=settings.SSL_CERTFILE
    ) 