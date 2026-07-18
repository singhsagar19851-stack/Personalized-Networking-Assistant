from unittest.mock import patch, MagicMock
from app.services import fact_checker


@patch("app.services.fact_checker.requests.get")
def test_fact_checker_returns_summary(mock_get):
    """Happy path: Wikipedia returns an extract."""

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "extract": "Artificial Intelligence is the simulation of human intelligence by machines."
    }

    mock_get.return_value = mock_response

    summary = fact_checker.fact_check("Artificial Intelligence")

    assert isinstance(summary, str)
    assert len(summary) > 10
    assert "Artificial Intelligence" in summary


@patch("app.services.fact_checker.requests.get")
def test_fact_checker_no_extract(mock_get):
    """Wikipedia responds successfully but has no extract."""

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}

    mock_get.return_value = mock_response

    summary = fact_checker.fact_check("Unknown Topic")

    assert isinstance(summary, str)
    assert summary != ""


@patch("app.services.fact_checker.requests.get")
def test_fact_checker_request_failure(mock_get):
    """Wikipedia request fails."""

    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.json.return_value = {}

    mock_get.return_value = mock_response

    summary = fact_checker.fact_check("Artificial Intelligence")

    assert isinstance(summary, str)
    assert summary != ""