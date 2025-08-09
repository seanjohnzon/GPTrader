from __future__ import annotations

from typing import Optional
from aiohttp import ClientSession

from gptrader.http import get_json


async def fetch_contract_score(session: ClientSession, contract: Optional[str]) -> tuple[str, Optional[int], bool]:
    """Fetch contract score from SolSniffer-like API.

    Returns tuple: (status_text, score_or_none, skip_bool)
    """
    if not contract:
        return ("No contract", None, True)

    url = f"https://api.solsniffer.com/v1/score/{contract}"
    try:
        data = await get_json(session, url)
        score = int(data.get("score", 0) or 0)
        status = f"Score {score}"
        return (status, score, False)
    except Exception as exc:
        return (f"Contract check error: {exc}", None, True)


