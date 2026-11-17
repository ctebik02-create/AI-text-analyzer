import pytest
import httpx
from unittest.mock import patch
from fastapi import HTTPException

from services.nvidia_service import get_ai_output

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

