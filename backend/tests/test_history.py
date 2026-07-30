import pytest
from httpx import AsyncClient


SAMPLE_TEXT = (
    "The government announced a new policy today regarding healthcare reform. "
    "Officials stated that the changes will take effect next year and aim to "
    "improve access to medical services for all citizens across the country."
)


@pytest.mark.asyncio
async def test_history_empty(client: AsyncClient, auth_headers):
    response = await client.get("/api/history", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0


@pytest.mark.asyncio
async def test_history_after_prediction(client: AsyncClient, auth_headers):
    predict_response = await client.post(
        "/api/predict",
        json={"text": SAMPLE_TEXT},
        headers=auth_headers,
    )
    assert predict_response.status_code == 201
    prediction_id = predict_response.json()["prediction"]["id"]

    response = await client.get("/api/history", headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert any(item["id"] == prediction_id for item in data["items"])


@pytest.mark.asyncio
async def test_delete_history_item(client: AsyncClient, auth_headers):
    predict_response = await client.post(
        "/api/predict",
        json={"text": SAMPLE_TEXT},
        headers=auth_headers,
    )
    prediction_id = predict_response.json()["prediction"]["id"]

    delete_response = await client.delete(
        f"/api/history/{prediction_id}",
        headers=auth_headers,
    )
    assert delete_response.status_code == 200

    history_response = await client.get("/api/history", headers=auth_headers)
    ids = [item["id"] for item in history_response.json()["items"]]
    assert prediction_id not in ids


@pytest.mark.asyncio
async def test_delete_nonexistent_history_item(client: AsyncClient, auth_headers):
    response = await client.delete("/api/history/99999", headers=auth_headers)
    assert response.status_code == 404
