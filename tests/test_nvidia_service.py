import pytest
import httpx
from httpx import AsyncClient
from unittest.mock import patch
from fastapi import HTTPException
from httpx import ASGITransport
from main import app
from services.nvidia_service import get_ai_output
from storage.orm_base import count_analyses_for_test


@pytest.mark.asyncio
async def test_nvidia_http_500():
    def mock_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=500,
        json={"error": "Server unavailable"})

    transport = httpx.MockTransport(mock_handler)

    real_async_client = httpx.AsyncClient

    def create_mock_client(*args, **kwargs):
        return real_async_client(transport=transport, **kwargs)

    with patch(
        "services.nvidia_service.AsyncClient",
        side_effect = create_mock_client):

        with pytest.raises(HTTPException) as exc_info:
            await get_ai_output("I like this product")

        assert exc_info.value.status_code == 502


@pytest.mark.asyncio
async def test_nvidia_http_timeout():
    def mock_handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("Request timed out")
    transport = httpx.MockTransport(mock_handler)
    real_async_client = httpx.AsyncClient

    def create_mock_client(*args, **kwargs):
        return real_async_client(transport=transport, **kwargs)
    with patch(
        "services.nvidia_service.AsyncClient",
        side_effect = create_mock_client
    ):
        with pytest.raises(HTTPException) as exc_info:
            await get_ai_output("I like this product")

        assert exc_info.value.status_code == 504

@pytest.mark.asyncio
async def test_post_analyze_nvidia_500():
    def mock_handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            status_code=500,
            json={"error": "Server unavailable"}
        )
    transport = httpx.MockTransport(mock_handler)
    real_async_client = httpx.AsyncClient
    def create_mock_client(*args, **kwargs):
        return real_async_client(transport=transport, **kwargs)
    with patch(
        "services.nvidia_service.AsyncClient",
        side_effect = create_mock_client):
        async with AsyncClient(
            transport=ASGITransport(app=app), base_url="http://test"
        ) as ac:
            count_before = await count_analyses_for_test()

            response = await ac.post("/analysis", json={
                "text": "I like this product"
            })

            count_after = await count_analyses_for_test()
            assert response.status_code == 502
            assert count_before == count_after

