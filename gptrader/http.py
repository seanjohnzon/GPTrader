from __future__ import annotations

import asyncio
from typing import Any
from aiohttp import ClientSession, ClientTimeout
from tenacity import retry, stop_after_attempt, wait_exponential_jitter


DEFAULT_TIMEOUT = ClientTimeout(total=15)


def default_headers() -> dict[str, str]:
    return {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/125.0.0.0 Safari/537.36"
        )
    }


@retry(stop=stop_after_attempt(3), wait=wait_exponential_jitter(0.5, 2.0))
async def get_text(session: ClientSession, url: str) -> str:
    async with session.get(url, headers=default_headers(), timeout=DEFAULT_TIMEOUT) as resp:
        resp.raise_for_status()
        return await resp.text()


@retry(stop=stop_after_attempt(3), wait=wait_exponential_jitter(0.5, 2.0))
async def get_json(session: ClientSession, url: str) -> Any:
    async with session.get(url, headers=default_headers(), timeout=DEFAULT_TIMEOUT) as resp:
        resp.raise_for_status()
        return await resp.json(content_type=None)


