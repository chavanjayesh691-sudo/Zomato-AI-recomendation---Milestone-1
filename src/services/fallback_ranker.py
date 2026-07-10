from typing import List

import pandas as pd


def fallback_rank(candidates: pd.DataFrame, k: int = 5) -> List[dict]:
    if candidates.empty:
        return []

    df = candidates.sort_values(by=["rating", "votes"], ascending=[False, False]).head(k)
    recommendations = []

    for rank, (_, row) in enumerate(df.iterrows(), start=1):
        explanation = (
            f"{row['name']} is a top-rated option with a {row['rating']} rating "
            f"and estimated cost ₹{row['cost_for_two']} for two."
        )
        recommendations.append(
            {
                "restaurant_id": str(row["id"]),
                "rank": rank,
                "explanation": explanation,
            }
        )

    return recommendations
