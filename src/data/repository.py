from __future__ import annotations
from typing import List

import pandas as pd
from src.data.preprocessor import preprocess_dataframe


class RestaurantRepository:
    def __init__(self, df: pd.DataFrame):
        if not df.empty and ("rating" not in df.columns or "cost_for_two" not in df.columns):
            df = preprocess_dataframe(df)
        self.df = df


    def query_by_location(self, location: str) -> pd.DataFrame:
        loc_lower = location.strip().lower()
        mask = self.df["location"] == loc_lower
        if "listed_in(city)" in self.df.columns:
            mask = mask | (self.df["listed_in(city)"].astype(str).str.strip().str.lower() == loc_lower)
        return self.df[mask]

    def query_by_cuisine(self, cuisine: str) -> pd.DataFrame:
        cuisine_list = [c.strip().lower() for c in cuisine.split(",") if c.strip()]
        def match_cuisine(cs):
            if cs is None:
                return False
            if isinstance(cs, str):
                cs_lower = cs.lower()
                return any(req in cs_lower for req in cuisine_list)
            try:
                return any(req in str(c).lower() for req in cuisine_list for c in cs)
            except TypeError:
                return any(req in str(cs).lower() for req in cuisine_list)
        return self.df[self.df["cuisines"].apply(match_cuisine)]

    def top_n_by_rating(self, n: int = 10) -> pd.DataFrame:
        sort_cols = [c for c in ["rating", "votes", "rate"] if c in self.df.columns]
        if sort_cols:
            return self.df.sort_values(by=sort_cols, ascending=[False] * len(sort_cols)).head(n)
        return self.df.head(n)


    def filter(self, location: str | None = None, cuisine: str | None = None, min_rating: float | None = None, budget_range: tuple | None = None) -> pd.DataFrame:
        df = self.df
        if location:
            loc_lower = location.strip().lower()
            mask = df["location"] == loc_lower
            if "listed_in(city)" in df.columns:
                mask = mask | (df["listed_in(city)"].astype(str).str.strip().str.lower() == loc_lower)
            df = df[mask]
        if cuisine:
            cuisine_list = [c.strip().lower() for c in cuisine.split(",") if c.strip()]
            def match_cuisine(cs):
                if cs is None:
                    return False
                if isinstance(cs, str):
                    cs_lower = cs.lower()
                    return any(req in cs_lower for req in cuisine_list)
                try:
                    return any(req in str(c).lower() for req in cuisine_list for c in cs)
                except TypeError:
                    return any(req in str(cs).lower() for req in cuisine_list)
            df = df[df["cuisines"].apply(match_cuisine)]


        if min_rating is not None:
            df = df[df["rating"] >= float(min_rating)]
        if budget_range is not None:
            low, high = budget_range
            df = df[df["cost_for_two"].apply(lambda c: c is not None and low <= c <= high)]
        return df
