from __future__ import annotations

from typing import List
from aiohttp import ClientSession

from gptrader.http import get_json
from gptrader.models import Coin


async def fetch_meteora_data(session: ClientSession) -> List[Coin]:
    url = "https://api.meteora.ag/pools"
    try:
        data = await get_json(session, url)
    except Exception:
        return []

    coins: List[Coin] = []
    if isinstance(data, list):
        for pool in data:
            name = pool.get("tokenSymbol") or pool.get("symbol") or "Unknown"
            coins.append(
                Coin(
                    platform="meteora.ag",
                    name=name,
                    tvl=pool.get("tvl", 0) or 0,
                    apy=pool.get("apy", 0) or 0,
                    twitter=pool.get("twitter"),
                    contract=pool.get("tokenAddress") or pool.get("mint") or None,
                )
            )
    return coins


