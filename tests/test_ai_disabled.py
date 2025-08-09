from __future__ import annotations

from gptrader.ai.evaluator import build_client, evaluate_coin_with_gpt
from gptrader.models import Coin


def test_ai_disabled_returns_message():
    client = build_client(None)
    coin = Coin(platform="test", name="TEST")
    result = evaluate_coin_with_gpt(client, coin, model="gpt-4o-mini")
    assert "AI disabled" in result


