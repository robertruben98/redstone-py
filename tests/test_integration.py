"""Live integration test against the real, keyless RedStone API.

Deselected by default (see ``addopts`` in ``pyproject.toml``). Run explicitly
with ``pytest -m integration``.
"""

import pytest

from redstone import PricePoint, RedStoneClient


@pytest.mark.integration
def test_live_get_price_eth():
    with RedStoneClient() as client:
        point = client.get_price("ETH")

    assert isinstance(point, PricePoint)
    assert point.symbol == "ETH"
    assert point.value > 0
    assert point.timestamp > 0
