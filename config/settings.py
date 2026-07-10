import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATASET_NAME = os.getenv("DATASET_NAME", "ManikaSaini/zomato-restaurant-recommendation")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
MAX_CANDIDATES = int(os.getenv("MAX_CANDIDATES", "30"))
TOP_K_RECOMMENDATIONS = int(os.getenv("TOP_K_RECOMMENDATIONS", "5"))
APP_TITLE = os.getenv("APP_TITLE", "AI Restaurant Recommender")

BUDGET_TIERS = {
    "low": (0, 500),
    "medium": (501, 1500),
    "high": (1501, float("inf")),
}

# Standard localities/places present in the dataset location field, required for user input later on
AVAILABLE_LOCATIONS = [
    "indiranagar",
    "bellandur",
    "btm",
    "hsr",
    "whitefield",
    "jayanagar",
    "jp nagar",
    "marathahalli",
    "bannerghatta road",
    "koramangala 5th block",
    "electronic city",
    "brigade road",
    "sarjapur road",
    "mg road",
    "banashankari",
]

