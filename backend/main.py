"""Main FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Import routers
from backend.api import auth, schema_changes, comments, notifications

app = FastAPI(
    title="ChangeGuard API",
    description="Schema and API change tracking platform",
    version="0.1.0"
)

# CORS middleware
origins = os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(schema_changes.router, prefix="/api/v1/schema-changes", tags=["schema-changes"])
app.include_router(comments.router, prefix="/api/v1/comments", tags=["comments"])
app.include_router(notifications.router, prefix="/api/v1/notifications", tags=["notifications"])

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "changeguard"}

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "ChangeGuard API",
        "version": "0.1.0",
        "docs": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8080)),
        reload=os.getenv("ENV") == "development"
    )
