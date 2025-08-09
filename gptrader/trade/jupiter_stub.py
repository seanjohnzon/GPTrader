from __future__ import annotations

from gptrader.models import Coin


def auto_trade(coin: Coin, enable_trading: bool, buy_amount_sol: float) -> None:
    if not enable_trading:
        print(
            f"[DRY RUN] Would BUY {buy_amount_sol} SOL of {coin.name} "
            f"@ {coin.price if coin.price is not None else 'N/A'}"
        )
        print("[DRY RUN] Set SLIPPAGE to configured value, profit target at multiplier.")
        print("[DRY RUN] Auto-sell at target, retain moonbag percentage.")
        return

    # LIVE TRADING LOGIC PLACEHOLDER
    # Integrate with Jupiter aggregator and Solana key management when enabled.
    pass


