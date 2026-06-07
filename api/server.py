"""
FastAPI Server - Main API application
"""
from fastapi import FastAPI, HTTPException, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from contextlib import asynccontextmanager
from loguru import logger
import uvicorn
import json
from pathlib import Path
from datetime import datetime
from typing import Optional

from config.settings import settings
from .routes import router
from .schemas import (
    BusinessIdea, PipelineResponse, MarketResearchResponse,
    ErrorResponse, HealthResponse
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info("Starting AI Agent Ecosystem API")
    
    # Initialize on startup
    Path("reports").mkdir(exist_ok=True)
    Path("generated_projects").mkdir(exist_ok=True)
    
    yield
    
    # Cleanup on shutdown
    logger.info("Shutting down AI Agent Ecosystem API")


# Create FastAPI app
app = FastAPI(
    title="AI Agent Ecosystem API",
    description="Multi-agent AI system for market research and product development",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api/v1")


@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "name": "AI Agent Ecosystem API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/api/v1/health"
    }


@app.get("/api/v1/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    from orchestrator.execution_engine import AgentOrchestrator
    
    try:
        orchestrator = AgentOrchestrator()
        agent_count = len(orchestrator.agents)
        
        return HealthResponse(
            status="healthy",
            agents_available=agent_count,
            api_key_configured=bool(settings.OPENAI_API_KEY),
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="unhealthy",
            agents_available=0,
            api_key_configured=False,
            timestamp=datetime.now().isoformat()
        )


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )


if __name__ == "__main__":
    uvicorn.run(
        "api.server:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=True,
        log_level=settings.LOG_LEVEL.lower()
    )