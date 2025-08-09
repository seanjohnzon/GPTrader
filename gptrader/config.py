from __future__ import annotations

import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv


class Settings(BaseModel):
    """Application settings loaded from environment variables."""

    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")
    gpt_model: str = Field(default="gpt-4o-mini", alias="GPT_MODEL")
    enable_ai: bool = Field(default=False, alias="ENABLE_AI")

    enable_trading: bool = Field(default=False, alias="ENABLE_TRADING")
    buy_amount_sol: float = Field(default=1.0, alias="BUY_AMOUNT_SOL")
    slippage: float = Field(default=0.15, alias="SLIPPAGE")
    profit_target_multiplier: int = Field(default=10, alias="PROFIT_TARGET_MULTIPLIER")
    moonbag_percentage: float = Field(default=0.2, alias="MOONBAG_PERCENTAGE")

    solana_rpc_url: Optional[str] = Field(default=None, alias="SOLANA_RPC_URL")
    private_key: Optional[str] = Field(default=None, alias="PRIVATE_KEY")

    contract_score_min: int = Field(default=85, alias="CONTRACT_SCORE_MIN")

    class Config:
        populate_by_name = True


def get_settings() -> Settings:
    """Load settings from .env and environment.

    Returns:
        Settings: Configured settings instance.
    """

    # Reason: Load .env before reading environment for local development.
    load_dotenv(override=False)
    env = {k: v for k, v in os.environ.items()}
    return Settings.model_validate(env)


