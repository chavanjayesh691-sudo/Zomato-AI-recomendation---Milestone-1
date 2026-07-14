from __future__ import annotations
import logging
from pathlib import Path
from typing import Optional, List

import pandas as pd

from config.settings import PROJECT_ROOT, GROQ_API_KEY, BUDGET_TIERS, AVAILABLE_LOCATIONS
from src.data.loader import load_or_cache_dataset
from src.data.repository import RestaurantRepository
from src.models.api_schemas import (
    RecommendationRequest,
    MetadataResponse,
    HealthResponse,
)
from src.models.recommendation import RecommendationResponse
from src.services.filter_service import FilterService
from src.services.llm_engine import LlmEngine
from src.services.orchestrator import RecommendationOrchestrator

logger = logging.getLogger(__name__)


class BackendService:
    """Unified backend service controller orchestrating dataset access, filtering, and LLM recommendations."""

    def __init__(
        self,
        repository: Optional[RestaurantRepository] = None,
        filter_service: Optional[FilterService] = None,
        llm_engine: Optional[LlmEngine] = None,
        orchestrator: Optional[RecommendationOrchestrator] = None,
        cache_path: Optional[Path] = None,
    ):
        self._df: Optional[pd.DataFrame] = None
        self.repository = repository
        self.filter_service = filter_service
        self.llm_engine = llm_engine
        self.orchestrator = orchestrator

        if self.repository is None:
            self._load_repository(cache_path)

        if self.filter_service is None and self.repository is not None:
            self.filter_service = FilterService(self.repository)

        if self.llm_engine is None:
            self.llm_engine = LlmEngine()

        if self.orchestrator is None and self.filter_service is not None and self.llm_engine is not None:
            self.orchestrator = RecommendationOrchestrator(self.filter_service, self.llm_engine)

        self._available_locations: List[str] = []
        self._available_cuisines: List[str] = []
        self._initialize_metadata()

    def _load_repository(self, cache_path: Optional[Path] = None):
        """Load dataframe from parquet cache or dataset loader."""
        if cache_path is None:
            # Check standard cached parquet paths in project root
            for filename in ["restaraunt.parquet", "restaurant.parquet"]:
                candidate = PROJECT_ROOT / filename
                if candidate.exists():
                    cache_path = candidate
                    break
            if cache_path is None:
                cache_path = PROJECT_ROOT / "restaraunt.parquet"

        try:
            self._df = load_or_cache_dataset(cache_path=cache_path)
            self.repository = RestaurantRepository(self._df)
        except Exception as e:
            logger.error(f"Failed to load dataset repository: {e}")
            self._df = pd.DataFrame()
            self.repository = RestaurantRepository(self._df)

    def _initialize_metadata(self):
        """Compute unique locations and top cuisines from the repository."""
        if self.repository is not None and not self.repository.df.empty:
            df = self.repository.df
            # Locations
            if "location" in df.columns:
                locs = df["location"].dropna().astype(str).str.strip()
                unique_locs = sorted([loc for loc in locs.unique() if loc])
                self._available_locations = unique_locs if unique_locs else AVAILABLE_LOCATIONS
            else:
                self._available_locations = AVAILABLE_LOCATIONS

            # Cuisines
            if "cuisines" in df.columns:
                cuisines_set = set()
                for item in df["cuisines"].dropna():
                    if isinstance(item, list):
                        for c in item:
                            if isinstance(c, str) and c.strip():
                                cuisines_set.add(c.strip())
                    elif isinstance(item, str):
                        for c in item.split(","):
                            if c.strip():
                                cuisines_set.add(c.strip())
                self._available_cuisines = sorted(list(cuisines_set))
        else:
            self._available_locations = AVAILABLE_LOCATIONS
            self._available_cuisines = []

    def recommend(self, request: RecommendationRequest) -> RecommendationResponse:
        """Execute end-to-end recommendation workflow from structured request."""
        if self.orchestrator is None:
            return RecommendationResponse(
                summary="Orchestrator unavailable.",
                recommendations=[],
                total_matches=0,
                filters_applied={},
                fallback_used=True,
            )

        preferences = request.to_user_preferences()
        return self.orchestrator.recommend(preferences, top_k=request.top_k)

    def get_metadata(self) -> MetadataResponse:
        """Return available filtering locations, cuisines, and dataset stats."""
        total = len(self.repository.df) if self.repository is not None else 0
        return MetadataResponse(
            available_locations=self._available_locations,
            available_cuisines=self._available_cuisines,
            total_restaurants=total,
            budget_tiers=BUDGET_TIERS,
        )

    def health_check(self) -> HealthResponse:
        """Check status of dataset repository and LLM engine readiness."""
        loaded = bool(self.repository is not None and not self.repository.df.empty)
        total = len(self.repository.df) if loaded else 0
        llm_ready = bool(GROQ_API_KEY and len(GROQ_API_KEY.strip()) > 0)
        status = "ok" if loaded else "degraded"
        return HealthResponse(
            status=status,
            dataset_loaded=loaded,
            total_records=total,
            llm_configured=llm_ready,
        )


import threading

_backend_service_singleton: Optional[BackendService] = None
_backend_service_lock = threading.Lock()


def get_backend_service() -> BackendService:
    """Singleton accessor for FastAPI dependency injection."""
    global _backend_service_singleton
    if _backend_service_singleton is None:
        with _backend_service_lock:
            if _backend_service_singleton is None:
                _backend_service_singleton = BackendService()
    return _backend_service_singleton


def reset_backend_service_singleton():
    """Reset singleton instance (useful for unit tests)."""
    global _backend_service_singleton
    with _backend_service_lock:
        _backend_service_singleton = None
