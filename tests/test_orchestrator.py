import pandas as pd

from src.data.preprocessor import preprocess_dataframe
from src.data.repository import RestaurantRepository
from src.models.preferences import UserPreferences
from src.services.filter_service import FilterService
from src.services.llm_engine import LlmEngine
from src.services.orchestrator import RecommendationOrchestrator


class DummyLlmEngine(LlmEngine):
    def __init__(self):
        self.client = None
        self.model = "dummy"

    def rank(self, prompt: str) -> dict:
        return {
            "summary": "Top matches for your preferences.",
            "recommendations": [
                {"restaurant_id": "0", "rank": 1, "explanation": "Excellent option."},
            ],
        }


def make_sample_df():
    return pd.DataFrame([
        {"name": "Alpha Bistro", "location": "Bengaluru", "cuisines": "Italian, Pizza", "rate": "4.5/5", "approx_cost(for two people)": "₹1200", "votes": "100"},
    ])


def test_orchestrator_uses_llm_output():
    df = preprocess_dataframe(make_sample_df())
    repo = RestaurantRepository(df)
    filter_service = FilterService(repo)
    llm_engine = DummyLlmEngine()
    orchestrator = RecommendationOrchestrator(filter_service, llm_engine)

    preferences = UserPreferences(
        location="Bangalore",
        budget="medium",
        cuisine="italian",
        min_rating=4.0,
        additional_preferences="",
    )

    result = orchestrator.recommend(preferences)
    assert result.summary == "Top matches for your preferences."
    assert len(result.recommendations) == 1
    assert result.recommendations[0].name == "Alpha Bistro"
