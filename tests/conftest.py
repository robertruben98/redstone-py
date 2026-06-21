"""Shared fixtures and sample payloads for the test suite."""

import pytest

SINGLE_PRICE_PAYLOAD = [
    {
        "id": "608fa2d2-0655-4815-9563-aa57e32b092c",
        "symbol": "ETH",
        "provider": "I-5rWUehEv-MjdK9gFw09RxfSLQX9DIHxG614Wf8qo0",
        "value": 1726.410429,
        "timestamp": 1782074280000,
        "liteEvmSignature": "deadbeef",
        "source": {"binance-usdt": 1726.410429, "okx-usd": 1726.64},
    }
]

MULTI_PRICE_PAYLOAD = {
    "ETH": {
        "symbol": "ETH",
        "provider": "I-5rWUehEv-MjdK9gFw09RxfSLQX9DIHxG614Wf8qo0",
        "value": 1726.47,
        "timestamp": 1782074320000,
    },
    "BTC": {
        "symbol": "BTC",
        "provider": "I-5rWUehEv-MjdK9gFw09RxfSLQX9DIHxG614Wf8qo0",
        "value": 65000.0,
        "timestamp": 1782074320000,
    },
}

HISTORICAL_PAYLOAD = [
    {"symbol": "ETH", "value": 1732.40, "timestamp": 1782070680000},
    {"symbol": "ETH", "value": 1726.41, "timestamp": 1782074280000},
]


@pytest.fixture
def single_price_payload():
    return SINGLE_PRICE_PAYLOAD


@pytest.fixture
def multi_price_payload():
    return MULTI_PRICE_PAYLOAD


@pytest.fixture
def historical_payload():
    return HISTORICAL_PAYLOAD
