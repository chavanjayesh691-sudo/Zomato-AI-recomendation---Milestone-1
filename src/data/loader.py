from __future__ import annotations
import os
from pathlib import Path
from typing import Optional

from datasets import load_dataset
import pandas as pd

from src.data.preprocessor import preprocess_dataframe


def load_zomato_dataset(dataset_name: str = "ManikaSaini/zomato-restaurant-recommendation", split: Optional[str] = "train") -> pd.DataFrame:
    """Load the Zomato dataset from Hugging Face and return a pandas DataFrame.

    The function attempts to load the dataset and returns an empty DataFrame on failure.
    """
    try:
        ds = load_dataset(dataset_name, split=split)
        df = ds.to_pandas()
        return df
    except Exception:
        return pd.DataFrame()


def save_to_parquet(df: pd.DataFrame, file_path: str | Path = "restaraunt.parquet") -> bool:
    """Save a DataFrame to a Parquet file for caching and faster cold starts."""
    try:
        df.to_parquet(file_path, index=False)
        return True
    except Exception:
        return False


def load_or_cache_dataset(
    cache_path: str | Path = "restaraunt.parquet",
    dataset_name: str = "ManikaSaini/zomato-restaurant-recommendation",
    split: Optional[str] = "train",
    preprocess: bool = True,
) -> pd.DataFrame:
    """Load the dataset from a Parquet cache if available; otherwise load from Hugging Face, preprocess, and cache it."""
    cache_file = Path(cache_path)
    if cache_file.exists():
        try:
            df = pd.read_parquet(cache_file)
            if preprocess and ("rating" not in df.columns or "cost_for_two" not in df.columns):
                df = preprocess_dataframe(df)
                save_to_parquet(df, cache_file)
            return df
        except Exception:
            pass


    df = load_zomato_dataset(dataset_name=dataset_name, split=split)
    if df.empty:
        return df

    if preprocess:
        df = preprocess_dataframe(df)

    save_to_parquet(df, cache_file)
    return df
