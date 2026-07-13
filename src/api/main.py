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
    logger.info("Starting non-blocking background thread to initialize BackendService...")
    import threading

    def _warmup():
        try:
            service = get_backend_service()
            logger.info("BackendService initialized successfully in background thread.")
        except Exception as e:
            logger.error(f"Error initializing BackendService in background thread: {e}")

    threading.Thread(target=_warmup, daemon=True).start()
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


if __name__ == "__main__":
    import os
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    logger.info(f"Starting Uvicorn server on 0.0.0.0:{port}")
    uvicorn.run("src.api.main:app", host="0.0.0.0", port=port)

