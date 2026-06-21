"""Internal helpers shared by the sync and async clients.

These functions build the query parameters and parse the JSON bodies for the
RedStone ``/prices`` endpoint. They are kept transport-agnostic so the sync and
async clients can share identical request/response semantics.
"""

from collections.abc import Sequence
from typing import Any, Optional

from .exceptions import RedStoneNotFoundError
from .models import PricePoint

PRICES_PATH = "/prices"
DEFAULT_PROVIDER = "redstone"


def single_price_params(symbol: str, provider: str) -> dict[str, Any]:
    """Build query params for the latest price of one symbol."""
    return {"symbol": symbol, "provider": provider, "limit": 1}


def multi_price_params(symbols: Sequence[str], provider: str) -> dict[str, Any]:
    """Build query params for the latest prices of several symbols."""
    return {"symbols": ",".join(symbols), "provider": provider}


def historical_params(
    symbol: str,
    provider: str,
    from_timestamp: int,
    to_timestamp: int,
    interval: Optional[int],
) -> dict[str, Any]:
    """Build query params for a historical price range query."""
    params: dict[str, Any] = {
        "symbol": symbol,
        "provider": provider,
        "fromTimestamp": from_timestamp,
        "toTimestamp": to_timestamp,
    }
    if interval is not None:
        params["interval"] = interval
    return params


def parse_single(data: Any, symbol: str) -> PricePoint:
    """Parse a single-symbol response, raising if no data is present."""
    if isinstance(data, list):
        if not data:
            raise RedStoneNotFoundError(f"No price data available for symbol {symbol!r}.")
        return PricePoint.model_validate(data[0])
    if isinstance(data, dict) and symbol in data:
        return PricePoint.model_validate(data[symbol])
    raise RedStoneNotFoundError(f"No price data available for symbol {symbol!r}.")


def parse_multi(data: Any) -> dict[str, PricePoint]:
    """Parse a multi-symbol response into a ``symbol -> PricePoint`` mapping."""
    if not isinstance(data, dict):
        return {}
    return {symbol: PricePoint.model_validate(point) for symbol, point in data.items()}


def parse_historical(data: Any) -> list[PricePoint]:
    """Parse a historical range response into a list of price points."""
    if not isinstance(data, list):
        return []
    return [PricePoint.model_validate(point) for point in data]
