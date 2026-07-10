import pandas as pd

from config.settings import BUDGET_TIERS
from src.data.preprocessor import preprocess_dataframe
from src.data.repository import RestaurantRepository
from src.models.preferences import UserPreferences
from src.services.filter_service import FilterService


def make_sample_df():
    return pd.DataFrame([
        {"name": "Alpha Bistro", "location": "Bengaluru", "cuisines": "Italian, Pizza", "rate": "4.5/5", "approx_cost(for two people)": "₹1200", "votes": "100"},
        {"name": "Beta Cafe", "location": "Bangalore", "cuisines": "Chinese", "rate": "4.0/5", "approx_cost(for two people)": "₹400", "votes": "50"},
        {"name": "Gamma Grill", "location": "Delhi", "cuisines": "North Indian", "rate": "4.2/5", "approx_cost(for two people)": "₹800", "votes": "70"},
    ])


def test_filter_service_applies_filters():
    df = preprocess_dataframe(make_sample_df())
    repo = RestaurantRepository(df)
    service = FilterService(repo)

    prefs = UserPreferences(
        location="Bangalore",
        budget="medium",
        cuisine="italian",
        min_rating=4.0,
        additional_preferences="",
    )

    result = service.filter_candidates(prefs)
    assert result["total_matches"] == 1
    assert result["candidates"].iloc[0]["name"] == "Alpha Bistro"
    assert result["filters_applied"]["location"] == "bangalore"
    assert result["filters_applied"]["budget_range"] == BUDGET_TIERS["medium"]
