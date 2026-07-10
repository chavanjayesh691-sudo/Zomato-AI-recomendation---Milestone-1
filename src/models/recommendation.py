from __future__ import annotations
from typing import List, Optional, Dict, Any
from pydantic import BaseModel


class Recommendation(BaseModel):
    rank: int
    name: str
    cuisine: str
    rating: float
    estimated_cost: str
    explanation: str


class RecommendationResponse(BaseModel):
    summary: Optional[str] = None
    recommendations: List[Recommendation] = []
    total_matches: int = 0
    filters_applied: Dict[str, Any] = {}
    fallback_used: bool = False

