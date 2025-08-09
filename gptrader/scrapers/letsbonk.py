from __future__ import annotations

from typing import List
from bs4 import BeautifulSoup
from aiohttp import ClientSession

from gptrader.http import get_text
from gptrader.models import Coin


async def fetch_letsbonk_data(session: ClientSession) -> List[Coin]:
    url = "https://letsbonk.fun/board"
    try:
        html = await get_text(session, url)
    except Exception:
        return []

    soup = BeautifulSoup(html, "html.parser")
    coins: List[Coin] = []
    for row in soup.select("div.coin-row"):
        name_el = row.select_one(".coin-name")
        price_el = row.select_one(".price")
        mc_el = row.select_one(".marketcap")

        name = name_el.text.strip() if name_el else "Unknown"
        price = None
        marketcap = None
        if price_el:
            try:
                price = float(price_el.text.replace("$", "").replace(",", "").strip())
            except Exception:
                price = None
        if mc_el:
            try:
                marketcap = float(mc_el.text.replace("$", "").replace(",", "").strip())
            except Exception:
                marketcap = None

        contract = row.get("data-contract")
        twitter_url = None
        socials = row.select_one(".socials a")
        if socials and socials.has_attr("href") and "twitter.com" in socials["href"]:
            twitter_url = socials["href"]

        coins.append(
            Coin(
                platform="letsbonk.fun",
                name=name,
                price=price,
                marketcap=marketcap,
                twitter=twitter_url,
                contract=contract,
            )
        )
    return coins


