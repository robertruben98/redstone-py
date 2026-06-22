# redstone-py

[![CI](https://github.com/robertruben98/redstone-py/actions/workflows/ci.yml/badge.svg)](https://github.com/robertruben98/redstone-py/actions/workflows/ci.yml)
[![PyPI version](https://img.shields.io/pypi/v/redstone-py.svg)](https://pypi.org/project/redstone-py/)
[![Docs](https://img.shields.io/badge/docs-online-blue)](https://robertruben98.github.io/redstone-py/)
[![Python versions](https://img.shields.io/pypi/pyversions/redstone-py.svg)](https://pypi.org/project/redstone-py/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Checked with mypy](https://img.shields.io/badge/mypy-strict-blue.svg)](https://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A small, fully typed Python client for the [RedStone](https://redstone.finance) oracle HTTP
API — RedStone's modular **pull** model price feeds. Sync **and** async, built on
[httpx](https://www.python-httpx.org/) and [pydantic v2](https://docs.pydantic.dev/).

> The public RedStone cache API is keyless, so you can fetch prices without any credentials.

## Installation

```bash
pip install redstone-py
```

The package installs as `redstone-py` and is imported as `redstone`:

```python
from redstone import RedStoneClient
```

## Quickstart

```python
from redstone import RedStoneClient

with RedStoneClient() as client:
    # Plain latest value as a float
    eth = client.get_latest_value("ETH")
    print(f"ETH = ${eth:,.2f}")

    # Full price point (value, timestamp, per-venue sources, signature, ...)
    point = client.get_price("BTC")
    print(point.value, point.timestamp)

    # Several symbols at once -> {symbol: PricePoint}
    prices = client.get_prices(["ETH", "BTC", "AVAX"])
    for symbol, p in prices.items():
        print(symbol, p.value)

    # Historical range (timestamps are Unix epoch in milliseconds)
    history = client.get_historical_prices(
        "ETH",
        from_timestamp=1782070680000,
        to_timestamp=1782074280000,
        interval=3600000,  # hourly
    )
    print(len(history), "points")
```

## Async

The async client mirrors the sync API exactly:

```python
import asyncio
from redstone import AsyncRedStoneClient


async def main():
    async with AsyncRedStoneClient() as client:
        value = await client.get_latest_value("ETH")
        print(value)


asyncio.run(main())
```

## API

Both `RedStoneClient` and `AsyncRedStoneClient` accept:

| Argument   | Default                          | Description                                         |
| ---------- | -------------------------------- | --------------------------------------------------- |
| `base_url` | `https://api.redstone.finance`   | RedStone API base URL.                              |
| `provider` | `redstone`                       | Default provider id (e.g. `redstone-primary-prod`). |
| `timeout`  | `30.0`                           | Per-request timeout in seconds.                     |
| `client`   | `None`                           | Bring your own `httpx.Client` / `AsyncClient`.      |

Methods (sync shown; the async client exposes the same names as coroutines):

- `get_price(symbol, provider=None) -> PricePoint`
- `get_latest_value(symbol, provider=None) -> float`
- `get_prices(symbols, provider=None) -> dict[str, PricePoint]`
- `get_historical_prices(symbol, from_timestamp, to_timestamp, interval=None, provider=None) -> list[PricePoint]`

### Errors

- `RedStoneError` — base class for all library errors.
- `RedStoneAPIError` — non-2xx HTTP response or transport failure (carries `status_code`).
- `RedStoneNotFoundError` — the requested symbol returned no data.

## Development

```bash
git clone https://github.com/robertruben98/redstone-py
cd redstone-py
pip install -e ".[dev]"
ruff check . && ruff format --check .
mypy --strict src tests
pytest                 # unit tests (live integration test deselected)
pytest -m integration  # run the live API test
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full workflow.

## License

[MIT](LICENSE)
