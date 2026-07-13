from __future__ import annotations
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config.settings import APP_TITLE, PROJECT_ROOT
from src.api.routes import router
from src.services.backend_service import get_backend_service

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing BackendService on startup...")
    try:
        service = get_backend_service()
        logger.info("BackendService initialized successfully.")
    except Exception as e:
        logger.error(f"Error initializing BackendService: {e}")
    yield
    logger.info("Application shutting down...")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance for Phase 4 & Phase 5."""
    app = FastAPI(
        title=APP_TITLE,
        description="Phase 4 & 5 Backend API and High-Quality Frontend Web Application for AI Restaurant Recommendations.",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Configure CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(router)

    # Mount static frontend web application
    frontend_dir = PROJECT_ROOT / "frontend"
    if frontend_dir.exists():
        from fastapi.staticfiles import StaticFiles
        app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")

    return app


app = create_app()

