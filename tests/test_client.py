"""Tests for the synchronous RedStone client (respx-mocked)."""

import httpx
import pytest
import respx

from redstone import RedStoneAPIError, RedStoneClient, RedStoneNotFoundError
from redstone.models import PricePoint

BASE_URL = "https://api.redstone.finance"


@respx.mock
def test_get_price_returns_price_point(single_price_payload):
    route = respx.get(f"{BASE_URL}/prices").mock(
        return_value=httpx.Response(200, json=single_price_payload)
    )

    with RedStoneClient() as client:
        point = client.get_price("ETH")

    assert isinstance(point, PricePoint)
    assert point.symbol == "ETH"
    assert point.value == 1726.410429
    request = route.calls.last.request
    assert request.url.params["symbol"] == "ETH"
    assert request.url.params["provider"] == "redstone"
    assert request.url.params["limit"] == "1"


@respx.mock
def test_get_price_respects_custom_provider(single_price_payload):
    route = respx.get(f"{BASE_URL}/prices").mock(
        return_value=httpx.Response(200, json=single_price_payload)
    )

    with RedStoneClient() as client:
        client.get_price("ETH", provider="redstone-primary-prod")

    assert route.calls.last.request.url.params["provider"] == "redstone-primary-prod"


@respx.mock
def test_get_latest_value_returns_float(single_price_payload):
    respx.get(f"{BASE_URL}/prices").mock(
        return_value=httpx.Response(200, json=single_price_payload)
    )

    with RedStoneClient() as client:
        value = client.get_latest_value("ETH")

    assert value == 1726.410429


@respx.mock
def test_get_prices_returns_mapping(multi_price_payload):
    route = respx.get(f"{BASE_URL}/prices").mock(
        return_value=httpx.Response(200, json=multi_price_payload)
    )

    with RedStoneClient() as client:
        prices = client.get_prices(["ETH", "BTC"])

    assert set(prices) == {"ETH", "BTC"}
    assert prices["BTC"].value == 65000.0
    assert route.calls.last.request.url.params["symbols"] == "ETH,BTC"


@respx.mock
def test_get_historical_prices_returns_list(historical_payload):
    route = respx.get(f"{BASE_URL}/prices").mock(
        return_value=httpx.Response(200, json=historical_payload)
    )

    with RedStoneClient() as client:
        points = client.get_historical_prices(
            "ETH", from_timestamp=1782070680000, to_timestamp=1782074280000, interval=3600000
        )

    assert len(points) == 2
    assert all(isinstance(p, PricePoint) for p in points)
    params = route.calls.last.request.url.params
    assert params["fromTimestamp"] == "1782070680000"
    assert params["toTimestamp"] == "1782074280000"
    assert params["interval"] == "3600000"


@respx.mock
def test_unknown_symbol_raises_not_found():
    respx.get(f"{BASE_URL}/prices").mock(return_value=httpx.Response(200, json=[]))

    with RedStoneClient() as client, pytest.raises(RedStoneNotFoundError):
        client.get_price("NOPE")


@respx.mock
def test_http_error_raises_api_error():
    respx.get(f"{BASE_URL}/prices").mock(return_value=httpx.Response(500, text="boom"))

    with RedStoneClient() as client, pytest.raises(RedStoneAPIError):
        client.get_price("ETH")


def test_custom_base_url_is_used():
    with RedStoneClient(base_url="https://example.test") as client:
        assert str(client.base_url).rstrip("/") == "https://example.test"
