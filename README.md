# GPTrader

Async Solana token discovery and evaluation bot with optional AI analysis and dry-run trading.

## Features
- Scrapers: Pump.fun, Meteora, LetsBonk
- Social check: Twitter widgets profile info (followers, verified, name changes)
- Risk: Contract scoring via SolSniffer (optional, fail-soft)
- AI: OpenAI GPT model for qualitative signals (configurable)
- Trading: Dry-run prints; live trading disabled by default

## Setup
1. Python 3.11+
2. Create venv and install deps:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Configure environment:
   ```bash
   cp .env.example .env
   # Fill OPENAI_API_KEY, SOLANA_RPC_URL, and PRIVATE_KEY if needed
   ```
4. Run:
   ```bash
   python -m gptrader
   ```

### Streamlit Dashboard
Run locally:
```bash
streamlit run app/streamlit_app.py
```
The dashboard lets you toggle AI/trading, adjust thresholds, and run a scan.

### Docker
Build and run with Docker Compose:
```bash
docker compose build
docker compose up
```
Open `http://localhost:8501`.

## Configuration
Environment variables (via `.env`):
- `OPENAI_API_KEY`: OpenAI API key (optional; AI disabled if missing)
- `GPT_MODEL`: e.g., `gpt-4o-mini`
- `ENABLE_AI`: `true|false` (default false)
- `ENABLE_TRADING`: `false` (default)
- `BUY_AMOUNT_SOL`, `SLIPPAGE`, `PROFIT_TARGET_MULTIPLIER`, `MOONBAG_PERCENTAGE`
- `SOLANA_RPC_URL`, `PRIVATE_KEY` (only for future live trading)

## Tests
```bash
pytest -q
```

## Notes
- External endpoints may change; scrapers include guards and retries.
- Twitter widgets endpoint is rate-limited; failures degrade gracefully.

## References
- Thread context and safety notes derived from community resources, including unroll of the original discussion and warnings about AI-poisoning risks. See: [Unrolled thread](https://unrollnow.com/status/1861118317676666914?utm_source=openai)


