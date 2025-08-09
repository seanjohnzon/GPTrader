from __future__ import annotations

import re
from typing import Optional
from aiohttp import ClientSession

from gptrader.http import get_json


def extract_username(twitter_url: Optional[str]) -> Optional[str]:
    if not twitter_url:
        return None
    match = re.search(r"twitter.com/([A-Za-z0-9_]+)", twitter_url)
    if not match:
        return None
    return match.group(1)


async def check_twitter_profile(session: ClientSession, twitter_url: Optional[str]) -> tuple[str, bool]:
    """Check twitter profile via public widgets API.

    Returns a tuple of (status_string, flagged_bool).
    """
    username = extract_username(twitter_url)
    if not username:
        return ("No or invalid Twitter link", False)

    api_url = (
        "https://cdn.syndication.twimg.com/widgets/followbutton/info.json?screen_names="
        f"{username}"
    )

    try:
        data = await get_json(session, api_url)
    except Exception as exc:
        return (f"Twitter check error: {exc}", False)

    if not data:
        return ("Account not found", False)

    try:
        profile = data[0]
        followers = int(profile.get("followers_count", 0) or 0)
        name_changes = int(profile.get("name_change_count", 0) or 0)
        verified = bool(profile.get("verified", False))
    except Exception:
        return ("Invalid profile data", False)

    trust_flag = "⚠️" if name_changes > 2 else "✅"
    flagged = name_changes > 2
    status = (
        f"Followers: {followers}, Verified: {verified}, Name changes: {name_changes} {trust_flag}"
    )
    return (status, flagged)


