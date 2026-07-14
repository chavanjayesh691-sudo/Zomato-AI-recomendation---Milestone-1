from __future__ import annotations
from typing import Any, Optional

from src.models.preferences import UserPreferences
from src.models.recommendation import RecommendationResponse, Recommendation
from src.services.filter_service import FilterService
from src.services.llm_engine import LlmEngine
from src.services.prompt_builder import build_recommendation_prompt
from src.services.fallback_ranker import fallback_rank


def _format_cuisines(val: Any) -> str:
    if val is None:
        return ""
    if isinstance(val, str):
        return val
    try:
        return ", ".join(str(x) for x in val if x)
    except TypeError:
        return str(val)



class RecommendationOrchestrator:
    def __init__(self, filter_service: FilterService, llm_engine: LlmEngine):
        self.filter_service = filter_service
        self.llm_engine = llm_engine

    def recommend(self, preferences: UserPreferences, top_k: Optional[int] = None) -> RecommendationResponse:
        filtered = self.filter_service.filter_candidates(preferences)
        candidates = filtered["candidates"]

        response = RecommendationResponse(
            summary=None,
            recommendations=[],
            total_matches=filtered["total_matches"],
            filters_applied=filtered["filters_applied"],
            fallback_used=False,
        )

        if candidates.empty:
            return response

        prompt = build_recommendation_prompt(preferences, candidates.to_dict(orient="records"))

        try:
            llm_output = self.llm_engine.rank(prompt)
            summary = llm_output.get("summary")
            recommendations = llm_output.get("recommendations", [])
            response.summary = summary

            candidate_map = {str(row["id"]): row for _, row in candidates.iterrows()}
            for item in recommendations:
                restaurant_id = str(item.get("restaurant_id", ""))
                rank = int(item.get("rank", 0))
                explanation = item.get("explanation", "")
                restaurant = candidate_map.get(restaurant_id)
                if restaurant is None or not explanation:
                    continue
                response.recommendations.append(
                    Recommendation(
                        rank=rank,
                        name=str(restaurant["name"]),
                        cuisine=_format_cuisines(restaurant["cuisines"]),
                        rating=float(restaurant["rating"] or 0.0),
                        estimated_cost=f"₹{restaurant['cost_for_two']} for two" if restaurant["cost_for_two"] is not None else "",
                        explanation=explanation,
                    )
                )
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(f"Groq LLM ranking failed: {e}. Falling back to deterministic ranking.")
            response.fallback_used = True
            recommendations = fallback_rank(candidates)
            response.summary = f"Recommendations generated from rule-based fallback ranking (LLM info: {e})."
            candidate_map = {str(row["id"]): row for _, row in candidates.iterrows()}
            for item in recommendations:
                restaurant_id = str(item.get("restaurant_id", ""))
                restaurant = candidate_map.get(restaurant_id)
                if restaurant is None:
                    continue
                response.recommendations.append(
                    Recommendation(
                        rank=item["rank"],
                        name=str(restaurant["name"]),
                        cuisine=_format_cuisines(restaurant["cuisines"]),
                        rating=float(restaurant["rating"] or 0.0),
                        estimated_cost=f"₹{restaurant['cost_for_two']} for two" if restaurant["cost_for_two"] is not None else "",
                        explanation=item["explanation"],
                    )
                )

        if top_k is not None and top_k > 0:
            response.recommendations = response.recommendations[:top_k]

        return response

