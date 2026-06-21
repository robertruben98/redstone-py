"""Synchronous quickstart for redstone-py.

Run with:
    python examples/quickstart.py
"""

from redstone import RedStoneClient


def main() -> None:
    with RedStoneClient() as client:
        eth = client.get_latest_value("ETH")
        print(f"ETH = ${eth:,.2f}")

        prices = client.get_prices(["ETH", "BTC"])
        for symbol, point in prices.items():
            print(f"{symbol}: {point.value} @ {point.timestamp}")


if __name__ == "__main__":
    main()
