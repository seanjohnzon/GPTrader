## Project Plan: GPTrader

### Goals
- Discover new Solana tokens from multiple sources, evaluate risk and social signals, optionally run AI analysis, and (optionally) execute trades using strict safeguards.

### Architecture
- `gptrader/config.py`: Central pydantic settings layer backed by `.env`.
- `gptrader/models.py`: Typed data models for tokens and evaluations.
- `gptrader/scrapers/`: Source-specific data collectors (Pump.fun, Meteora, LetsBonk).
- `gptrader/social/twitter.py`: Twitter credibility checks via public widgets API.
- `gptrader/risk/contract_score.py`: Optional contract scoring providers (SolSniffer, pluggable).
- `gptrader/ai/evaluator.py`: OpenAI-based analysis with configurable model.
- `gptrader/trade/jupiter_stub.py`: Dry-run trading logic; live trading disabled by default.
- `gptrader/orchestrator.py`: Async orchestration of the pipeline.
- `gptrader/__main__.py`: CLI entry point (`python -m gptrader`).

### Conventions
- Python 3.11+, PEP8, `black` formatting, type hints.
- Pydantic for validation, aiohttp for async HTTP.
- Tests in `tests/` mirroring structure. Each module has: success, edge, and failure tests.
- No file > 500 LOC; split into modules when approaching the limit.

### Safety & Config
- All secrets in `.env` (never committed). Trading disabled unless `ENABLE_TRADING=true`.
- Timeouts, retries with jitter, and fail-soft behavior for external APIs.
- Rate limits and concurrency caps to avoid hammering endpoints.


