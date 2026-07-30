import pytest
from httpx import AsyncClient


@pytest.fixture
def sample_text():
    return (
        "The government announced a new policy today regarding healthcare reform. "
        "Officials stated that the changes will take effect next year."
    )


@pytest.mark.asyncio
async def test_dashboard_empty(client: AsyncClient, auth_headers):
    response = await client.get("/api/dashboard", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["stats"]["total_predictions"] == 0
    assert data["stats"]["fake_count"] == 0
    assert data["stats"]["real_count"] == 0
    assert data["recent_predictions"] == []


@pytest.mark.asyncio
async def test_dashboard_with_predictions(client: AsyncClient, auth_headers, sample_text):
    await client.post(
        "/api/predict",
        json={"text": sample_text * 3},
        headers=auth_headers,
    )

    response = await client.get("/api/dashboard", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["stats"]["total_predictions"] >= 1
    assert len(data["recent_predictions"]) >= 1
    assert "trend" in data
