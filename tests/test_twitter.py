from __future__ import annotations

import pytest

from gptrader.social.twitter import extract_username


@pytest.mark.parametrize(
    "url,expected",
    [
        ("https://twitter.com/elonmusk", "elonmusk"),
        ("https://x.com/elonmusk", None),
        (None, None),
        ("https://twitter.com/Some_User123", "Some_User123"),
    ],
)
def test_extract_username(url, expected):
    assert extract_username(url) == expected


