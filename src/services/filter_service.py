from __future__ import annotations
from typing import Any

from config.settings import BUDGET_TIERS, MAX_CANDIDATES
from src.data.preprocessor import normalize_location
from src.data.repository import RestaurantRepository
from src.models.preferences import UserPreferences



class FilterService:
    def __init__(self, repository: RestaurantRepository):
        self.repository = repository

    def budget_range(self, budget: Any) -> tuple[int, float] | None:
        if isinstance(budget, (int, float)):
            val = float(budget)
            for tier, (low, high) in BUDGET_TIERS.items():
                if low <= val <= high:
                    return (low, high)
            return None
        if isinstance(budget, str):
            b_clean = budget.strip().lower()
            if b_clean in BUDGET_TIERS:
                return BUDGET_TIERS[b_clean]
            try:
                val = float(b_clean)
                for tier, (low, high) in BUDGET_TIERS.items():
                    if low <= val <= high:
                        return (low, high)
            except ValueError:
                pass
        return None

    def normalize_cuisine(self, cuisine: Any) -> str | None:
        if cuisine is None:
            return None
        if isinstance(cuisine, list):
            cuisine = ",".join(cuisine)
        if not isinstance(cuisine, str):
            return None
        cleaned = cuisine.strip().lower()
        if not cleaned or cleaned in {"any", "all", "none", "n/a"}:
            return None
        return cleaned

    def build_filters(self, preferences: UserPreferences) -> dict[str, Any]:
        cuisine = self.normalize_cuisine(preferences.cuisine)
        return {
            "location": normalize_location(preferences.location) if preferences.location else None,
            "cuisine": cuisine,
            "min_rating": preferences.min_rating,
            "budget_range": self.budget_range(preferences.budget),
        }


    def filter_candidates(self, preferences: UserPreferences) -> dict[str, Any]:
        filters = self.build_filters(preferences)
        filtered = self.repository.filter(
            location=filters["location"],
            cuisine=filters["cuisine"],
            min_rating=filters["min_rating"],
            budget_range=filters["budget_range"],
        )

        sort_cols = [c for c in ["rating", "votes", "rate"] if c in filtered.columns]
        if sort_cols:
            sorted_df = filtered.sort_values(by=sort_cols, ascending=[False] * len(sort_cols))
        else:
            sorted_df = filtered
        candidates = sorted_df.head(MAX_CANDIDATES)


        return {
            "candidates": candidates,
            "total_matches": len(filtered),
            "filters_applied": filters,
        }
