from __future__ import annotations

from typing import Optional
from pydantic import BaseModel, Field


class Coin(BaseModel):
    platform: str
    name: str
    price: Optional[float] = None
    marketcap: Optional[float] = None
    tvl: Optional[float] = None
    apy: Optional[float] = None
    twitter: Optional[str] = None
    contract: Optional[str] = None

    twitter_check: Optional[str] = None
    contract_check: Optional[str] = None
    contract_score: Optional[int] = None
    flagged: bool = False
    skip: bool = False
    gpt_analysis: Optional[str] = None


class Evaluation(BaseModel):
    summary: str
    profit_potential: int = Field(ge=1, le=10)


