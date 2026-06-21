"""Tests for the pydantic models that parse RedStone API responses."""

from redstone.models import PricePoint


def test_price_point_parses_single_price_payload():
    payload = {
        "id": "608fa2d2-0655-4815-9563-aa57e32b092c",
        "symbol": "ETH",
        "provider": "I-5rWUehEv-MjdK9gFw09RxfSLQX9DIHxG614Wf8qo0",
        "value": 1726.410429,
        "timestamp": 1782074280000,
        "liteEvmSignature": "deadbeef",
        "source": {"binance-usdt": 1726.410429, "okx-usd": 1726.64},
    }

    point = PricePoint.model_validate(payload)

    assert point.symbol == "ETH"
    assert point.value == 1726.410429
    assert point.provider == "I-5rWUehEv-MjdK9gFw09RxfSLQX9DIHxG614Wf8qo0"
    assert point.timestamp == 1782074280000
    assert point.source is not None
    assert point.source["okx-usd"] == 1726.64


def test_price_point_handles_missing_optional_fields():
    payload = {"symbol": "BTC", "value": 65000.0, "timestamp": 1782074280000}

    point = PricePoint.model_validate(payload)

    assert point.symbol == "BTC"
    assert point.id is None
    assert point.source is None
