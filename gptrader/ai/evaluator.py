from __future__ import annotations

from typing import Optional
from openai import OpenAI

from gptrader.models import Coin


def build_client(api_key: Optional[str]) -> Optional[OpenAI]:
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def build_prompt(coin: Coin) -> str:
    return (
        "Analyze this Solana-based coin:\n"
        f"Platform: {coin.platform}\n"
        f"Name: {coin.name}\n"
        f"Price: {coin.price if coin.price is not None else 'N/A'}\n"
        f"Market Cap: {coin.marketcap if coin.marketcap is not None else 'N/A'}\n"
        f"TVL: {coin.tvl if coin.tvl is not None else 'N/A'}\n"
        f"APY: {coin.apy if coin.apy is not None else 'N/A'}\n"
        f"Twitter Status: {coin.twitter_check or 'N/A'}\n"
        f"Contract Score: {coin.contract_check or 'N/A'}\n\n"
        "Check for signs of fake volume, repetitive rug behavior, and scam patterns. "
        "Rate profit potential from 1 to 10 and explain."
    )


def evaluate_coin_with_gpt(client: Optional[OpenAI], coin: Coin, model: str) -> str:
    if client is None:
        return "AI disabled or missing API key"

    prompt = build_prompt(coin)
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=200,
            timeout=20,
        )
        return resp.choices[0].message.content
    except Exception as exc:
        return f"AI evaluation failed for model '{model}': {exc}"


