from __future__ import annotations
from pathlib import Path
import time

from src.data.loader import load_or_cache_dataset


def main() -> None:
    print("Generating restaraunt.parquet cache from Zomato dataset...")
    start_time = time.time()
    
    # Generate and cache restaraunt.parquet
    df = load_or_cache_dataset(cache_path="restaraunt.parquet", preprocess=True)
    df.to_parquet("restaraunt.parquet", index=False)
    df.to_parquet("restaurant.parquet", index=False)
        
    elapsed = round(time.time() - start_time, 2)
    print(f"Successfully generated restaraunt.parquet ({len(df)} records) in {elapsed}s!")


if __name__ == "__main__":
    main()
