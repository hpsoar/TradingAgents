"""Configuration for optional China market providers."""

from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class ChinaMarketConfig:
    tushare_token: str | None = None
    request_timeout: int = 10
    max_news_items: int = 10


def get_config() -> ChinaMarketConfig:
    timeout_raw = os.getenv("CHINA_MARKET_TIMEOUT", "10")
    news_raw = os.getenv("CHINA_MARKET_NEWS_LIMIT", "10")
    try:
        timeout = max(1, int(timeout_raw))
    except ValueError:
        timeout = 10
    try:
        max_news_items = max(1, int(news_raw))
    except ValueError:
        max_news_items = 10

    return ChinaMarketConfig(
        tushare_token=os.getenv("TUSHARE_TOKEN") or None,
        request_timeout=timeout,
        max_news_items=max_news_items,
    )
