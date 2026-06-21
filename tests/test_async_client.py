"""Tests for the asynchronous RedStone client (respx-mocked)."""

import httpx
import pytest
import respx

from redstone import AsyncRedStoneClient, RedStoneAPIError, RedStoneNotFoundError
from redstone.models import PricePoint

BASE_URL = "https://api.redstone.finance"


@respx.mock
async def test_async_get_price_returns_price_point(single_price_payload):
    route = respx.get(f"{BASE_URL}/prices").mock(
        return_value=httpx.Response(200, json=single_price_payload)
    )

    async with AsyncRedStoneClient() as client:
        point = await client.get_price("ETH")

    assert isinstance(point, PricePoint)
    assert point.value == 1726.410429
    assert route.calls.last.request.url.params["limit"] == "1"


@respx.mock
async def test_async_get_latest_value_returns_float(single_price_payload):
    respx.get(f"{BASE_URL}/prices").mock(
        return_value=httpx.Response(200, json=single_price_payload)
    )

    async with AsyncRedStoneClient() as client:
        value = await client.get_latest_value("ETH")

    assert value == 1726.410429


@respx.mock
async def test_async_get_prices_returns_mapping(multi_price_payload):
    respx.get(f"{BASE_URL}/prices").mock(return_value=httpx.Response(200, json=multi_price_payload))

    async with AsyncRedStoneClient() as client:
        prices = await client.get_prices(["ETH", "BTC"])

    assert prices["ETH"].value == 1726.47


@respx.mock
async def test_async_get_historical_prices_returns_list(historical_payload):
    respx.get(f"{BASE_URL}/prices").mock(return_value=httpx.Response(200, json=historical_payload))

    async with AsyncRedStoneClient() as client:
        points = await client.get_historical_prices(
            "ETH", from_timestamp=1782070680000, to_timestamp=1782074280000
        )

    assert len(points) == 2


@respx.mock
async def test_async_unknown_symbol_raises_not_found():
    respx.get(f"{BASE_URL}/prices").mock(return_value=httpx.Response(200, json=[]))

    async with AsyncRedStoneClient() as client:
        with pytest.raises(RedStoneNotFoundError):
            await client.get_price("NOPE")


@respx.mock
async def test_async_http_error_raises_api_error():
    respx.get(f"{BASE_URL}/prices").mock(return_value=httpx.Response(503, text="down"))

    async with AsyncRedStoneClient() as client:
        with pytest.raises(RedStoneAPIError):
            await client.get_price("ETH")
