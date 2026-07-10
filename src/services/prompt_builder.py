import json
from typing import Any

from src.models.preferences import UserPreferences


def _serialize_preference(value: Any) -> Any:
    if isinstance(value, list):
        return [str(item).strip().lower() for item in value]
    if isinstance(value, str):
        return value.strip()
    return value


def build_recommendation_prompt(preferences: UserPreferences, candidates: list[dict]) -> str:
    preferences_payload = {
        "location": preferences.location.strip(),
        "budget": preferences.budget,
        "cuisine": _serialize_preference(preferences.cuisine),
        "min_rating": preferences.min_rating,
        "additional_preferences": preferences.additional_preferences or "",
    }

    candidate_rows = []
    for row in candidates:
        candidate_rows.append(
            {
                "id": str(row.get("id", "")),
                "name": str(row.get("name", "")).strip(),
                "cuisines": [str(x) for x in row.get("cuisines", [])] if row.get("cuisines") is not None else [],
                "rating": float(row.get("rating", 0) or 0),
                "cost_for_two": int(row.get("cost_for_two") or 0),
            }
        )

    prompt = (
        "You are an expert restaurant recommendation assistant. "
        "Only recommend restaurants from the provided candidate list. "
        "Do not invent or hallucinate any restaurant.\n\n"
        "User Preferences:\n"
        f"{json.dumps(preferences_payload, indent=2)}\n\n"
        "Candidate Restaurants:\n"
        f"{json.dumps(candidate_rows, indent=2)}\n\n"
        "Task:\n"
        "1. Select the top 5 restaurants that best match the user's preferences.\n"
        "2. Rank them from best to worst.\n"
        "3. For each recommended restaurant, include a short explanation tied to the user's preferences.\n"
        "4. Return valid JSON only, with the exact schema described below.\n\n"
        "Output schema:\n"
        "{\n"
        "  \"summary\": \"string\",\n"
        "  \"recommendations\": [\n"
        "    {\n"
        "      \"restaurant_id\": \"string\",\n"
        "      \"rank\": integer,\n"
        "      \"explanation\": \"string\"\n"
        "    }\n"
        "  ]\n"
        "}\n"
    )
    return prompt
