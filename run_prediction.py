import os
import json
from pathlib import Path
from dotenv import load_dotenv

from src.data.loader import load_or_cache_dataset
from src.data.repository import RestaurantRepository
from src.services.filter_service import FilterService
from src.services.llm_engine import LlmEngine
from src.services.orchestrator import RecommendationOrchestrator
from src.models.preferences import UserPreferences

import sys
sys.stdout.reconfigure(encoding='utf-8')

def main():
    load_dotenv()
    print("Loading restaurant dataset...")
    df = load_or_cache_dataset()
    print(f"Loaded dataset with {len(df)} restaurants.")
    
    repo = RestaurantRepository(df)
    filter_svc = FilterService(repo)
    llm = LlmEngine()
    orchestrator = RecommendationOrchestrator(filter_svc, llm)
    
    prefs = UserPreferences(
        location="Bellandur",
        min_rating=4.2,
        budget=1000,
        cuisine="",
        additional_preferences="Top 5 restaurants in Bellandur within budget 1000 with rating >= 4.2"
    )
    
    print("\nFiltering candidates and predicting top 5 restaurants using LLM...")
    res = orchestrator.recommend(prefs)
    
    print("\n=== RECOMMENDATION SUMMARY ===")
    print(f"Total Matches Found: {res.total_matches}")
    print(f"Filters Applied: {res.filters_applied}")
    print(f"Summary: {res.summary}\n")
    
    print("=== TOP 5 RESTAURANTS ===")
    for rec in res.recommendations:
        print(f"#{rec.rank}: {rec.name}")
        print(f"   Cuisine: {rec.cuisine}")
        print(f"   Rating: {rec.rating} / 5.0")
        print(f"   Estimated Cost: {rec.estimated_cost}")
        print(f"   Explanation: {rec.explanation}\n")

if __name__ == "__main__":
    main()
