from __future__ import annotations

import asyncio
from gptrader.orchestrator import run_once


def main() -> None:
    asyncio.run(run_once())


if __name__ == "__main__":
    main()


