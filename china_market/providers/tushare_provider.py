"""Tushare provider for optional enhanced A-share data."""

from __future__ import annotations

from typing import Any

from china_market.config import get_config
from china_market.models import DataResult
from china_market.providers.base import BaseChinaProvider
from china_market.symbols import NormalizedSymbol


class TushareProvider(BaseChinaProvider):
    name = "tushare"

    def __init__(self):
        self._ts: Any | None = None
        self._api: Any | None = None
        self._import_error: Exception | None = None
        self._token = get_config().tushare_token

    @property
    def api(self):
        if self._api is None and self._import_error is None and self._token:
            try:
                import tushare as ts
                ts.set_token(self._token)
                self._ts = ts
                self._api = ts.pro_api()
            except Exception as exc:  # pragma: no cover - provider availability path
                self._import_error = exc
        return self._api

    def is_available(self) -> bool:
        return self.api is not None

    def get_market_data(
        self, symbol: NormalizedSymbol, start_date: str, end_date: str
    ) -> DataResult:
        if not self._token:
            return DataResult.unavailable(
                "market_data",
                symbol.canonical,
                "TUSHARE_TOKEN is not configured; skipped Tushare.",
            )
        if not self.is_available():
            return self._not_available("market_data", symbol)
        data = self.api.daily(
            ts_code=symbol.tushare_symbol,
            start_date=start_date.replace("-", ""),
            end_date=end_date.replace("-", ""),
        )
        if data is None or data.empty:
            return DataResult.unavailable(
                "market_data", symbol.canonical, "Tushare returned no market rows."
            )
        return DataResult("market_data", symbol.canonical, "success", self.name, data)

    def get_company_info(self, symbol: NormalizedSymbol) -> DataResult:
        if not self._token:
            return DataResult.unavailable(
                "company_info",
                symbol.canonical,
                "TUSHARE_TOKEN is not configured; skipped Tushare.",
            )
        if not self.is_available():
            return self._not_available("company_info", symbol)
        data = self.api.stock_basic(ts_code=symbol.tushare_symbol)
        if data is None or data.empty:
            return DataResult.unavailable(
                "company_info", symbol.canonical, "Tushare returned no company info."
            )
        return DataResult("company_info", symbol.canonical, "success", self.name, data)

    def get_financial_info(self, symbol: NormalizedSymbol) -> DataResult:
        if not self._token:
            return DataResult.unavailable(
                "financial_info",
                symbol.canonical,
                "TUSHARE_TOKEN is not configured; skipped Tushare.",
            )
        if not self.is_available():
            return self._not_available("financial_info", symbol)
        data = self.api.fina_indicator(ts_code=symbol.tushare_symbol, limit=4)
        if data is None or data.empty:
            return DataResult.unavailable(
                "financial_info",
                symbol.canonical,
                "Tushare returned no financial indicators.",
            )
        return DataResult("financial_info", symbol.canonical, "success", self.name, data)

    def get_news_events(
        self, symbol: NormalizedSymbol, start_date: str | None = None,
        end_date: str | None = None, limit: int = 10
    ) -> DataResult:
        if not self._token:
            return DataResult.unavailable(
                "news_events",
                symbol.canonical,
                "TUSHARE_TOKEN is not configured; skipped Tushare news.",
            )
        if not self.is_available():
            return self._not_available("news_events", symbol)
        return DataResult.unavailable(
            "news_events",
            symbol.canonical,
            "Tushare news often requires separate permissions; use as optional enhancement.",
        )
