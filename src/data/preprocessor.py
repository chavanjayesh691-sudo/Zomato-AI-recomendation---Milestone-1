from __future__ import annotations
import re
from typing import Any

import pandas as pd


def normalize_location(loc: Any) -> str:
    if not isinstance(loc, str):
        return ""
    s = loc.strip().lower()
    for suffix in [", bangalore", ", bengaluru", ", karnataka", ", india", " bangalore", " bengaluru"]:
        if s.endswith(suffix) and len(s) > len(suffix):
            s = s[:-len(suffix)].strip().rstrip(",")
    aliases = {"bengaluru": "bangalore", "delhi ncr": "delhi"}
    return aliases.get(s, s)


def parse_rating(rate: Any) -> float | None:
    try:
        if isinstance(rate, (int, float)):
            return float(rate)
        if not isinstance(rate, str):
            return None
        m = re.search(r"([0-9]+\.?[0-9]*)", rate)
        if m:
            val = float(m.group(1))
            if 0 <= val <= 5:
                return val
        return None
    except Exception:
        return None


def parse_cost(cost: Any) -> int | None:
    try:
        if isinstance(cost, (int, float)):
            return int(cost)
        if not isinstance(cost, str):
            return None
        # Remove currency symbols and commas
        s = re.sub(r"[^0-9]", "", cost)
        if s == "":
            return None
        return int(s)
    except Exception:
        return None


def split_cuisines(cuisines_field: Any) -> list[str]:
    if not isinstance(cuisines_field, str):
        return []
    parts = [c.strip().lower() for c in cuisines_field.split(",") if c.strip()]
    return parts


def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize relevant fields and return a cleaned DataFrame."""
    if df.empty:
        return df

    df = df.copy()

    # Common raw field candidates
    name_fields = ["name", "restaurant_name", "Restaurant Name"]
    location_fields = ["location", "city", "listed_in(city)"]
    cuisine_fields = ["cuisines", "Cuisines", "cuisine"]
    rating_fields = ["rating", "rate", "aggregate_rating"]
    cost_fields = ["cost_for_two", "approx_cost(for two people)", "average_cost"]


    # Ensure name
    for f in name_fields:
        if f in df.columns:
            df["name"] = df[f].astype(str).str.strip()
            break
    df["name"] = df.get("name", "")

    # Location
    for f in location_fields:
        if f in df.columns:
            df["location"] = df[f].apply(normalize_location)
            break
    df["location"] = df.get("location", "")

    # Cuisines
    for f in cuisine_fields:
        if f in df.columns:
            df["cuisines"] = df[f].apply(split_cuisines)
            break
    df["cuisines"] = df.get("cuisines", [[]])

    # Rating
    for f in rating_fields:
        if f in df.columns:
            df["rating"] = df[f].apply(parse_rating)
            break
    df["rating"] = df.get("rating", None)

    # Cost
    for f in cost_fields:
        if f in df.columns:
            df["cost_for_two"] = df[f].apply(parse_cost)
            break
    df["cost_for_two"] = df.get("cost_for_two", None)

    # Votes
    if "votes" in df.columns:
        df["votes"] = pd.to_numeric(df["votes"], errors="coerce").fillna(0).astype(int)
    else:
        df["votes"] = 0

    # Ensure ID
    if "id" not in df.columns:
        df["id"] = df.index.astype(str)

    # Drop rows without a name
    df = df[df["name"].str.strip() != ""]

    # Keep only compact columns needed for filtering & recommendations
    keep_cols = ["id", "name", "location", "cuisines", "rating", "cost_for_two", "votes"]
    if "listed_in(city)" in df.columns:
        keep_cols.append("listed_in(city)")
    existing_cols = [c for c in keep_cols if c in df.columns]
    df = df[existing_cols]

    return df
