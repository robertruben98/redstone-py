"""redstone-py: a typed sync + async Python client for the RedStone oracle API.

Example:
    >>> from redstone import RedStoneClient
    >>> with RedStoneClient() as client:
    ...     client.get_latest_value("ETH")  # doctest: +SKIP
    1726.41
"""

from .async_client import AsyncRedStoneClient
from .client import RedStoneClient
from .exceptions import RedStoneAPIError, RedStoneError, RedStoneNotFoundError
from .models import PricePoint

__all__ = [
    "AsyncRedStoneClient",
    "PricePoint",
    "RedStoneAPIError",
    "RedStoneClient",
    "RedStoneError",
    "RedStoneNotFoundError",
]

__version__ = "0.1.0"
