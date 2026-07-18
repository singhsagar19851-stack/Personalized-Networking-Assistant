from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_generate_conversation_api():
    payload = {
        "description": "Sustainability in smart cities",
        "interests": ["green energy", "public transport"]
    }

    response = client.post("/generate-conversation", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "topics" in data
    assert "suggestions" in data
    assert isinstance(data["topics"], list)
    assert isinstance(data["suggestions"], list)


def test_fact_check_api():
    response = client.post(
        "/fact-check",
        json={"query": "Artificial Intelligence"}
    )

    assert response.status_code == 200

    data = response.json()

    assert "summary" in data
    assert isinstance(data["summary"], str)


def test_analyze_event_api():
    response = client.post(
        "/analyze-event",
        json={
            "description": "AI conference for healthcare innovation"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "topics" in data
    assert isinstance(data["topics"], list)


def test_invalid_generate_request_returns_422():
    response = client.post(
        "/generate-conversation",
        json={}
    )

    assert response.status_code == 422


def test_invalid_analyze_request_returns_422():
    response = client.post(
        "/analyze-event",
        json={}
    )

    assert response.status_code == 422


def test_invalid_fact_check_request_returns_422():
    response = client.post(
        "/fact-check",
        json={}
    )

    assert response.status_code == 422