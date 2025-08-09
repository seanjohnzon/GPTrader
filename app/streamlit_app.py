from __future__ import annotations

import asyncio
from typing import List

import pandas as pd
import streamlit as st

from gptrader.config import Settings, get_settings
from gptrader.models import Coin
from gptrader.orchestrator import collect_and_evaluate


st.set_page_config(page_title="GPTrader Dashboard", layout="wide", initial_sidebar_state="expanded")
st.title("GPTrader Dashboard")

with st.sidebar:
    st.header("Run Settings")
    base = get_settings()
    enable_ai = st.checkbox("Enable AI", value=base.enable_ai)
    enable_trading = st.checkbox("Enable Trading (danger)", value=base.enable_trading)
    # Model selection mapping
    model_options = {
        "GPT-4o mini (fast/cheap)": "gpt-4o-mini",
        "GPT-4o": "gpt-4o",
        "GPT-5 (if available)": "gpt-5",
    }
    # Determine default label based on current config
    default_label = next(
        (label for label, mid in model_options.items() if mid == base.gpt_model),
        "GPT-4o mini (fast/cheap)",
    )
    options = list(model_options.keys())
    try:
        default_index = options.index(default_label)
    except ValueError:
        default_index = 0
    selected_label = st.selectbox("OpenAI Model", options=options, index=default_index)
    selected_model = model_options[selected_label]
    contract_min = st.number_input(
        "Min Contract Score", min_value=0, max_value=100, value=base.contract_score_min, step=5
    )
    buy_amount = st.number_input(
        "Buy Amount (SOL)", min_value=0.0, value=float(base.buy_amount_sol), step=0.5
    )
    run_btn = st.button("Run Scan")


def coins_to_df(coins: List[Coin]) -> pd.DataFrame:
    rows = []
    for c in coins:
        rows.append(
            {
                "platform": c.platform,
                "name": c.name,
                "price": c.price,
                "marketcap": c.marketcap,
                "tvl": c.tvl,
                "apy": c.apy,
                "twitter_check": c.twitter_check,
                "contract_check": c.contract_check,
                "contract_score": c.contract_score,
                "flagged": c.flagged,
                "skip": c.skip,
                "gpt_analysis": c.gpt_analysis,
            }
        )
    return pd.DataFrame(rows)


if run_btn:
    st.info("Running scan... this may take a moment.")
    override = Settings.model_validate(
        {
            "ENABLE_AI": str(enable_ai).lower(),
            "ENABLE_TRADING": str(enable_trading).lower(),
            "CONTRACT_SCORE_MIN": contract_min,
            "BUY_AMOUNT_SOL": buy_amount,
            "GPT_MODEL": selected_model,
        }
    )
    coins = asyncio.run(collect_and_evaluate(override))
    st.success(f"Scan complete: {len(coins)} evaluated tokens")

    if coins:
        df = coins_to_df(coins)
        st.dataframe(df, use_container_width=True)
    else:
        st.write("No tokens found.")
else:
    st.write("Click 'Run Scan' to start.")


