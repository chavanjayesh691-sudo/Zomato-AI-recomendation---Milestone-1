from __future__ import annotations
import logging
from fastapi import APIRouter, Depends, HTTPException, status

from src.models.api_schemas import (
    RecommendationRequest,
    MetadataResponse,
    HealthResponse,
    ErrorResponse,
)
from src.models.recommendation import RecommendationResponse
from src.services.backend_service import BackendService, get_backend_service

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/api/v1/recommend",
    response_model=RecommendationResponse,
    status_code=status.HTTP_200_OK,
    summary="Search & Rank Restaurant Recommendations",
    description="Accepts structured user preferences, applies deterministic filtering, and invokes LLM (or rule-based fallback) to return ranked recommendations.",
    responses={
        500: {"model": ErrorResponse, "description": "Internal server error during recommendation workflow."}
    },
)
def recommend_restaurants(
    request: RecommendationRequest,
    service: BackendService = Depends(get_backend_service),
) -> RecommendationResponse:
    try:
        return service.recommend(request)
    except Exception as e:
        logger.exception(f"Error during recommend_restaurants: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Recommendation workflow failed: {e}",
        )


@router.get(
    "/api/v1/metadata",
    response_model=MetadataResponse,
    status_code=status.HTTP_200_OK,
    summary="Get Filtering Metadata",
    description="Returns available locations, cuisine options, total dataset records, and budget tier configurations.",
)
def get_metadata(
    service: BackendService = Depends(get_backend_service),
) -> MetadataResponse:
    return service.get_metadata()


@router.get(
    "/api/v1/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="API Health Check",
    description="Check readiness of the dataset repository and LLM service configuration.",
)
@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    include_in_schema=False,
)
def health_check(
    service: BackendService = Depends(get_backend_service),
) -> HealthResponse:
    return service.health_check()
