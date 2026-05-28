"""
CiberActuar Backend — FastAPI Application Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.api.v1 import scan, quote, recalculate
from app.core.config import settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info("🚀 CiberActuar Backend starting...")
    yield
    logger.info("🛑 CiberActuar Backend shutting down...")


app = FastAPI(
    title="CiberActuar API",
    description="Cybersecurity risk scoring and insurance quoting for SMEs",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# CORS — allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(scan.router, prefix="/api/v1", tags=["scan"])
app.include_router(quote.router, prefix="/api/v1", tags=["quote"])
app.include_router(recalculate.router, prefix="/api/v1", tags=["recalculate"])


@app.get("/")
async def root():
    return {
        "app": "CiberActuar API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
