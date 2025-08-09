from __future__ import annotations

import asyncio
from typing import List
from aiohttp import ClientSession

from gptrader.config import get_settings, Settings
from gptrader.models import Coin
from gptrader.scrapers.pumpfun import fetch_pumpfun_data
from gptrader.scrapers.meteora import fetch_meteora_data
from gptrader.scrapers.letsbonk import fetch_letsbonk_data
from gptrader.social.twitter import check_twitter_profile
from gptrader.risk.contract_score import fetch_contract_score
from gptrader.ai.evaluator import build_client, evaluate_coin_with_gpt
from gptrader.trade.jupiter_stub import auto_trade


async def collect_and_evaluate(settings: Settings | None = None) -> List[Coin]:
    if settings is None:
        settings = get_settings()
    client = build_client(settings.openai_api_key) if settings.enable_ai else None

    async with ClientSession() as session:
        scrape_tasks = [
            fetch_pumpfun_data(session),
            fetch_meteora_data(session),
            fetch_letsbonk_data(session),
        ]
        results = await asyncio.gather(*scrape_tasks, return_exceptions=True)

        all_coins: List[Coin] = []
        for res in results:
            if isinstance(res, Exception):
                continue
            all_coins.extend(res)

        evaluated: List[Coin] = []
        for coin in all_coins:
            status, score, _ = await fetch_contract_score(session, coin.contract)
            coin.contract_score = score
            coin.contract_check = (status + (" ✅" if score and score >= settings.contract_score_min else " ❌")) if score is not None else status
            if score is None or score < settings.contract_score_min:
                coin.skip = True

            twitter_status, flagged = await check_twitter_profile(session, coin.twitter)
            coin.twitter_check = twitter_status
            coin.flagged = flagged

            if coin.skip:
                coin.gpt_analysis = "Skipped due to low contract score or missing data"
            else:
                coin.gpt_analysis = evaluate_coin_with_gpt(client, coin, settings.gpt_model)

            if not coin.skip:
                auto_trade(coin, settings.enable_trading, settings.buy_amount_sol)

            evaluated.append(coin)
            await asyncio.sleep(0.5)

        return evaluated


async def run_once() -> None:
    settings = get_settings()
    evaluated = await collect_and_evaluate(settings)
    print(f"\n[INFO] Collected {len(evaluated)} evaluated coins.")
    print("\n=== TOP COINS (AI-evaluated, Contract & Social Checked) ===")
    for coin in evaluated:
        if coin.skip:
            continue
        flagged = "🚩" if coin.flagged else ""
        print(
            f"{coin.name} ({coin.platform}) {flagged}\n-> {coin.gpt_analysis}\n-> Twitter: {coin.twitter_check}\n-> Contract: {coin.contract_check}\n"
        )


