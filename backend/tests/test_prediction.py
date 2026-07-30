import pytest
from httpx import AsyncClient


SAMPLE_TEXT = (
    "The government announced a new policy today regarding healthcare reform. "
    "Officials stated that the changes will take effect next year and aim to "
    "improve access to medical services for all citizens across the country."
)


@pytest.mark.asyncio
async def test_cors_headers_for_localhost_dev_ports(client: AsyncClient):
    response = await client.options(
        "/api/predict",
        headers={
            "Origin": "http://localhost:5174",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "content-type",
        },
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:5174"
    assert response.headers.get("access-control-allow-credentials") == "true"


@pytest.mark.asyncio
async def test_predict(client: AsyncClient, auth_headers):
    response = await client.post(
        "/api/predict",
        json={"text": SAMPLE_TEXT},
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert "prediction" in data
    assert data["prediction"]["label_name"] == "Real"
    assert data["prediction"]["confidence"] == 0.87
    assert "explainability" in data
    assert "ai_analysis" in data


@pytest.mark.asyncio
async def test_predict_unauthorized(client: AsyncClient):
    response = await client.post(
        "/api/predict",
        json={"text": SAMPLE_TEXT},
    )
    assert response.status_code == 201
    data = response.json()
    assert "prediction" in data


@pytest.mark.asyncio
async def test_predict_text_too_short(client: AsyncClient, auth_headers):
    response = await client.post(
        "/api/predict",
        json={"text": "short"},
        headers=auth_headers,
    )
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_upload_txt(client: AsyncClient, auth_headers):
    files = {"file": ("article.txt", SAMPLE_TEXT.encode("utf-8"), "text/plain")}
    response = await client.post(
        "/api/upload",
        files=files,
        headers=auth_headers,
    )
    assert response.status_code == 201
    data = response.json()
    assert data["prediction"]["source"] == "upload"
