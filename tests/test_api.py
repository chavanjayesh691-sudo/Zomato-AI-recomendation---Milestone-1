import pandas as pd
from fastapi.testclient import TestClient

from src.api.main import app
from src.data.preprocessor import preprocess_dataframe
from src.data.repository import RestaurantRepository
from src.services.backend_service import BackendService, get_backend_service, get_backend_service_if_ready
from src.services.filter_service import FilterService
from src.services.llm_engine import LlmEngine
from src.services.orchestrator import RecommendationOrchestrator


class DummyLlmEngine(LlmEngine):
    def rank(self, prompt: str) -> dict:
        return {
            "summary": "API test recommendation summary.",
            "recommendations": [
                {"restaurant_id": "0", "rank": 1, "explanation": "Perfect dining spot."},
            ],
        }


def override_backend_service():
    df = preprocess_dataframe(
        pd.DataFrame([
            {
                "name": "Gamma Grill",
                "location": "Indiranagar",
                "cuisines": "Burgers, Fast Food",
                "rate": "4.4/5",
                "approx_cost(for two people)": "₹700",
                "votes": "150",
            }
        ])
    )
    repo = RestaurantRepository(df)
    filter_service = FilterService(repo)
    llm_engine = DummyLlmEngine()
    orchestrator = RecommendationOrchestrator(filter_service, llm_engine)
    return BackendService(
        repository=repo,
        filter_service=filter_service,
        llm_engine=llm_engine,
        orchestrator=orchestrator,
    )


app.dependency_overrides[get_backend_service] = override_backend_service
app.dependency_overrides[get_backend_service_if_ready] = override_backend_service
client = TestClient(app)


def test_health_check_endpoint():
    resp = client.get("/api/v1/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["dataset_loaded"] is True
    assert data["total_records"] == 1


def test_metadata_endpoint():
    resp = client.get("/api/v1/metadata")
    assert resp.status_code == 200
    data = resp.json()
    assert data["total_restaurants"] == 1
    assert "indiranagar" in data["available_locations"]


def test_recommend_endpoint():
    payload = {
        "location": "Indiranagar",
        "budget_tier": "$$",
        "cuisines": "burgers",
        "min_rating": 4.0,
        "dietary_preferences": "outdoor seating",
        "top_k": 5,
    }
    resp = client.post("/api/v1/recommend", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["summary"] == "API test recommendation summary."
    assert len(data["recommendations"]) == 1
    assert data["recommendations"][0]["name"] == "Gamma Grill"
    assert data["fallback_used"] is False
