from __future__ import annotations
from typing import List, Optional, Union, Dict, Any
from pydantic import BaseModel, Field

from src.models.preferences import UserPreferences


class RecommendationRequest(BaseModel):
    """Structured request payload for recommendations."""
    location: str = Field(..., description="Target location or city alias (e.g. 'Bengaluru', 'Indiranagar')")
    budget_tier: Union[str, int, float] = Field(
        default="$$",
        description="Budget preference: '$', '$$', '$$$', '$$$$' or approximate cost numeric value"
    )
    cuisines: Union[str, List[str]] = Field(
        default="",
        description="Desired cuisines, either comma-separated string or list of strings"
    )
    min_rating: float = Field(
        default=0.0,
        ge=0.0,
        le=5.0,
        description="Minimum rating filter (0.0 to 5.0)"
    )
    dietary_preferences: Optional[str] = Field(
        default=None,
        description="Free-text preferences (e.g., 'romantic rooftop seating', 'pure veg dining')"
    )
    top_k: int = Field(
        default=10,
        ge=1,
        le=50,
        description="Maximum number of ranked recommendations to return"
    )

    def to_user_preferences(self) -> UserPreferences:
        """Convert API request schema to internal UserPreferences domain model."""
        return UserPreferences(
            location=self.location,
            budget=self.budget_tier,
            cuisine=self.cuisines,
            min_rating=self.min_rating,
            additional_preferences=self.dietary_preferences
        )


class MetadataResponse(BaseModel):
    """Metadata response containing available locations, cuisines, and dataset summary."""
    available_locations: List[str]
    available_cuisines: List[str]
    total_restaurants: int
    budget_tiers: Dict[str, Any]


class HealthResponse(BaseModel):
    """API health status response."""
    status: str
    dataset_loaded: bool
    total_records: int
    llm_configured: bool


class ErrorResponse(BaseModel):
    """Structured error response schema."""
    detail: str
    error_code: Optional[str] = None
