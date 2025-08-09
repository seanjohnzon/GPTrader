from __future__ import annotations

import os
from gptrader.config import get_settings


def test_default_settings_load():
    os.environ.pop("OPENAI_API_KEY", None)
    settings = get_settings()
    assert settings.enable_ai is False
    assert settings.enable_trading is False
    assert settings.gpt_model


