"""Exception hierarchy for redstone-py."""

from typing import Optional


class RedStoneError(Exception):
    """Base class for all errors raised by redstone-py."""


class RedStoneAPIError(RedStoneError):
    """Raised when the RedStone API returns a non-success HTTP status.

    Attributes:
        status_code: The HTTP status code returned by the API, if known.
    """

    def __init__(self, message: str, status_code: Optional[int] = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class RedStoneNotFoundError(RedStoneError):
    """Raised when a requested symbol has no available price data."""
