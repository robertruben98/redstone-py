"""Asynchronous client for the RedStone oracle HTTP API."""

from collections.abc import Sequence
from types import TracebackType
from typing import Any, Optional

import httpx

from . import _params
from .client import DEFAULT_BASE_URL, DEFAULT_TIMEOUT
from .exceptions import RedStoneAPIError
from .models import PricePoint


class AsyncRedStoneClient:
    """An asynchronous client for the RedStone oracle HTTP API.

    This mirrors :class:`~redstone.client.RedStoneClient` but exposes ``async``
    methods backed by :class:`httpx.AsyncClient`. Use it as an async context
    manager to ensure the connection pool is closed::

        async with AsyncRedStoneClient() as client:
            price = await client.get_latest_value("ETH")

    Args:
        base_url: Base URL of the RedStone API. Defaults to
            ``https://api.redstone.finance``.
        provider: Default provider id used when a method does not specify one.
            Defaults to ``"redstone"``.
        timeout: Per-request timeout in seconds.
        client: An optional pre-configured :class:`httpx.AsyncClient`. When
            supplied, the caller is responsible for closing it.
    """

    def __init__(
        self,
        base_url: str = DEFAULT_BASE_URL,
        provider: str = _params.DEFAULT_PROVIDER,
        timeout: float = DEFAULT_TIMEOUT,
        client: Optional[httpx.AsyncClient] = None,
    ) -> None:
        self.base_url = base_url
        self.provider = provider
        self._owns_client = client is None
        self._client = client or httpx.AsyncClient(base_url=base_url, timeout=timeout)

    async def __aenter__(self) -> "AsyncRedStoneClient":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> None:
        await self.aclose()

    async def aclose(self) -> None:
        """Close the underlying HTTP client if this instance owns it."""
        if self._owns_client:
            await self._client.aclose()

    async def _get(self, params: dict[str, Any]) -> Any:
        try:
            response = await self._client.get(_params.PRICES_PATH, params=params)
            response.raise_for_status()
        except httpx.HTTPStatusError as err:
            raise RedStoneAPIError(
                f"RedStone API returned HTTP {err.response.status_code}.",
                status_code=err.response.status_code,
            ) from err
        except httpx.HTTPError as err:
            raise RedStoneAPIError(f"RedStone API request failed: {err}") from err
        return response.json()

    async def get_price(self, symbol: str, provider: Optional[str] = None) -> PricePoint:
        """Fetch the latest price point for a single symbol.

        Args:
            symbol: The data-feed symbol to query, e.g. ``"ETH"``.
            provider: Provider id to query. Defaults to the client's provider.

        Returns:
            The latest :class:`~redstone.models.PricePoint` for the symbol.

        Raises:
            RedStoneNotFoundError: If no price data is available for the symbol.
            RedStoneAPIError: If the API returns an error response.
        """
        data = await self._get(_params.single_price_params(symbol, provider or self.provider))
        return _params.parse_single(data, symbol)

    async def get_latest_value(self, symbol: str, provider: Optional[str] = None) -> float:
        """Fetch just the latest aggregated price value for a symbol.

        Args:
            symbol: The data-feed symbol to query, e.g. ``"ETH"``.
            provider: Provider id to query. Defaults to the client's provider.

        Returns:
            The latest price as a ``float``.

        Raises:
            RedStoneNotFoundError: If no price data is available for the symbol.
            RedStoneAPIError: If the API returns an error response.
        """
        point = await self.get_price(symbol, provider=provider)
        return point.value

    async def get_prices(
        self, symbols: Sequence[str], provider: Optional[str] = None
    ) -> dict[str, PricePoint]:
        """Fetch the latest price points for several symbols at once.

        Args:
            symbols: The data-feed symbols to query, e.g. ``["ETH", "BTC"]``.
            provider: Provider id to query. Defaults to the client's provider.

        Returns:
            A mapping of symbol to its latest :class:`~redstone.models.PricePoint`.

        Raises:
            RedStoneAPIError: If the API returns an error response.
        """
        data = await self._get(_params.multi_price_params(symbols, provider or self.provider))
        return _params.parse_multi(data)

    async def get_historical_prices(
        self,
        symbol: str,
        from_timestamp: int,
        to_timestamp: int,
        interval: Optional[int] = None,
        provider: Optional[str] = None,
    ) -> list[PricePoint]:
        """Fetch historical price points for a symbol over a time range.

        Args:
            symbol: The data-feed symbol to query, e.g. ``"ETH"``.
            from_timestamp: Range start as a Unix epoch in milliseconds.
            to_timestamp: Range end as a Unix epoch in milliseconds.
            interval: Optional sampling interval in milliseconds (e.g.
                ``3600000`` for hourly).
            provider: Provider id to query. Defaults to the client's provider.

        Returns:
            A list of :class:`~redstone.models.PricePoint` ordered by the API.

        Raises:
            RedStoneAPIError: If the API returns an error response.
        """
        data = await self._get(
            _params.historical_params(
                symbol, provider or self.provider, from_timestamp, to_timestamp, interval
            )
        )
        return _params.parse_historical(data)
