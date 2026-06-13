"""Thin adapter used by TradingAgents' existing dataflow router."""

from __future__ import annotations

from functools import lru_cache

from china_market.manager import ChinaDataSourceManager
from china_market.symbols import normalize_symbol


_CHINA_METHODS = {
    "get_stock_data",
    "get_indicators",
    "get_fundamentals",
    "get_balance_sheet",
    "get_cashflow",
    "get_income_statement",
    "get_news",
}


def should_handle(method: str, *args) -> bool:
    if method not in _CHINA_METHODS or not args:
        return False
    return normalize_symbol(args[0]) is not None


def route_method(method: str, *args, **kwargs) -> str:
    manager = _get_manager()
    if method == "get_stock_data":
        return manager.get_market_data(args[0], args[1], args[2])
    if method == "get_indicators":
        return manager.get_indicators(args[0], args[1], args[2], args[3] if len(args) > 3 else 30)
    if method == "get_news":
        return manager.get_news_events(args[0], args[1], args[2])
    if method == "get_fundamentals":
        return manager.get_company_info(args[0]) + "\n\n" + manager.get_financial_info(args[0])
    if method in {"get_balance_sheet", "get_cashflow", "get_income_statement"}:
        return manager.get_financial_info(args[0])
    raise ValueError(f"china_market does not support method '{method}'")


@lru_cache(maxsize=1)
def _get_manager() -> ChinaDataSourceManager:
    return ChinaDataSourceManager()
