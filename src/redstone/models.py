"""Pydantic models describing RedStone oracle API responses."""

from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class PricePoint(BaseModel):
    """A single price observation returned by the RedStone oracle API.

    Each point represents the aggregated value of a data feed (``symbol``) as
    signed by a given ``provider`` at a specific ``timestamp``. The optional
    ``source`` map breaks the aggregate down into the individual venue prices
    that fed into it.

    Attributes:
        id: Server-assigned identifier for the price record, when present.
        symbol: The data-feed symbol, e.g. ``"ETH"`` or ``"BTC"``.
        provider: The provider identifier or public key that signed the value.
        value: The aggregated price expressed in the feed's quote currency.
        timestamp: Observation time as a Unix epoch in **milliseconds**.
        source: Optional per-venue prices keyed by ``"<exchange>-<quote>"``.
        lite_evm_signature: Optional lightweight EVM signature of the payload.
        permaweb_tx: Optional Arweave transaction id where the data is stored.
        provider_public_key: Optional public key of the signing provider.
    """

    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: Optional[str] = Field(default=None, description="Server-assigned price record id.")
    symbol: str = Field(description="Data-feed symbol, e.g. 'ETH'.")
    provider: Optional[str] = Field(
        default=None, description="Provider id or public key that signed the value."
    )
    value: float = Field(description="Aggregated price in the feed's quote currency.")
    timestamp: int = Field(description="Observation time as a Unix epoch in milliseconds.")
    source: Optional[dict[str, float]] = Field(
        default=None, description="Per-venue prices keyed by '<exchange>-<quote>'."
    )
    lite_evm_signature: Optional[str] = Field(
        default=None,
        alias="liteEvmSignature",
        description="Lightweight EVM signature of the payload.",
    )
    permaweb_tx: Optional[str] = Field(
        default=None,
        alias="permawebTx",
        description="Arweave transaction id where the data is stored.",
    )
    provider_public_key: Optional[str] = Field(
        default=None,
        alias="providerPublicKey",
        description="Public key of the signing provider.",
    )
