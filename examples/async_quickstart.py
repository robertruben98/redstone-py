"""Asynchronous quickstart for redstone-py.

Run with:
    python examples/async_quickstart.py
"""

import asyncio

from redstone import AsyncRedStoneClient


async def main() -> None:
    async with AsyncRedStoneClient() as client:
        eth = await client.get_latest_value("ETH")
        print(f"ETH = ${eth:,.2f}")

        prices = await client.get_prices(["ETH", "BTC"])
        for symbol, point in prices.items():
            print(f"{symbol}: {point.value} @ {point.timestamp}")


if __name__ == "__main__":
    asyncio.run(main())
