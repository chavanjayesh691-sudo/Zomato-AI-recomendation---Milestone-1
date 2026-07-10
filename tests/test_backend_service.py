import pandas as pd
import pytest

from src.data.preprocessor import preprocess_dataframe
from src.data.repository import RestaurantRepository
from src.models.api_schemas import RecommendationRequest
from src.services.backend_service import BackendService
from src.services.filter_service import FilterService
from src.services.llm_engine import LlmEngine
from src.services.orchestrator import RecommendationOrchestrator


class DummyLlmEngine(LlmEngine):
    def __init__(self):
        self.client = None
        self.model = "dummy"

    def rank(self, prompt: str) -> dict:
        return {
            "summary": "AI recommendation summary.",
            "recommendations": [
                {"restaurant_id": "0", "rank": 1, "explanation": "Top rated food and ambiance."},
                {"restaurant_id": "1", "rank": 2, "explanation": "Great value for money."},
            ],
        }


def make_sample_df():
    return pd.DataFrame([
        {
            "name": "Alpha Bistro",
            "location": "Bengaluru",
            "cuisines": "Italian, Pizza",
            "rate": "4.5/5",
            "approx_cost(for two people)": "₹1200",
            "votes": "100",
        },
        {
            "name": "Beta Diner",
            "location": "Bengaluru",
            "cuisines": "North Indian, Biryani",
            "rate": "4.2/5",
            "approx_cost(for two people)": "₹800",
            "votes": "80",
        },
    ])


def test_backend_service_recommendation_and_metadata():
    df = preprocess_dataframe(make_sample_df())
    repo = RestaurantRepository(df)
    filter_service = FilterService(repo)
    llm_engine = DummyLlmEngine()
    orchestrator = RecommendationOrchestrator(filter_service, llm_engine)

    service = BackendService(
        repository=repo,
        filter_service=filter_service,
        llm_engine=llm_engine,
        orchestrator=orchestrator,
    )

    # Test metadata
    meta = service.get_metadata()
    assert meta.total_restaurants == 2
    assert "bangalore" in meta.available_locations
    assert "italian" in meta.available_cuisines or "pizza" in meta.available_cuisines

    # Test health check
    health = service.health_check()
    assert health.status == "ok"
    assert health.dataset_loaded is True
    assert health.total_records == 2

    # Test recommend
    request = RecommendationRequest(
        location="Bengaluru",
        budget_tier="$$",
        cuisines="",
        min_rating=4.0,
        dietary_preferences=None,
        top_k=1,
    )
    response = service.recommend(request)
    assert response.summary == "AI recommendation summary."
    assert len(response.recommendations) == 1
    assert response.recommendations[0].name == "Alpha Bistro"
    assert response.fallback_used is False
