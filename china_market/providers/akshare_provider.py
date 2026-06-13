"""AkShare provider for A-share data."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from china_market.models import DataResult
from china_market.providers.base import BaseChinaProvider
from china_market.symbols import NormalizedSymbol


class AkShareProvider(BaseChinaProvider):
    name = "akshare"

    def __init__(self):
        self._ak: Any | None = None
        self._import_error: Exception | None = None

    @property
    def ak(self):
        if self._ak is None and self._import_error is None:
            try:
                import akshare as ak
                self._ak = ak
            except Exception as exc:  # pragma: no cover - exercised via manager fallback
                self._import_error = exc
        return self._ak

    def is_available(self) -> bool:
        return self.ak is not None

    def get_market_data(
        self, symbol: NormalizedSymbol, start_date: str, end_date: str
    ) -> DataResult:
        if not self.is_available():
            return self._not_available("market_data", symbol)

        data = self.ak.stock_zh_a_hist(
            symbol=symbol.code,
            period="daily",
            start_date=_date_compact(start_date),
            end_date=_date_compact(end_date),
            adjust="",
        )
        if data is None or data.empty:
            return DataResult.unavailable(
                "market_data", symbol.canonical, "AkShare returned no market rows."
            )
        return DataResult(
            kind="market_data",
            symbol=symbol.canonical,
            status="success",
            provider=self.name,
            data=data,
        )

    def get_company_info(self, symbol: NormalizedSymbol) -> DataResult:
        if not self.is_available():
            return self._not_available("company_info", symbol)

        data = self.ak.stock_individual_info_em(symbol=symbol.akshare_symbol)
        if data is None or data.empty:
            return DataResult.unavailable(
                "company_info", symbol.canonical, "AkShare returned no company info."
            )
        return DataResult("company_info", symbol.canonical, "success", self.name, data)

    def get_financial_info(self, symbol: NormalizedSymbol) -> DataResult:
        if not self.is_available():
            return self._not_available("financial_info", symbol)

        data = self.ak.stock_financial_abstract(symbol=symbol.code)
        if data is None or data.empty:
            return DataResult.unavailable(
                "financial_info",
                symbol.canonical,
                "AkShare returned no financial summary.",
            )
        return DataResult("financial_info", symbol.canonical, "success", self.name, data)

    def get_news_events(
        self, symbol: NormalizedSymbol, start_date: str | None = None,
        end_date: str | None = None, limit: int = 10
    ) -> DataResult:
        if not self.is_available():
            return self._not_available("news_events", symbol)

        data = self.ak.stock_news_em(symbol=symbol.code)
        if data is None or data.empty:
            return DataResult.unavailable(
                "news_events", symbol.canonical, "AkShare returned no news rows."
            )
        return DataResult(
            "news_events",
            symbol.canonical,
            "success",
            self.name,
            data.head(limit),
        )


def _date_compact(value: str) -> str:
    try:
        return datetime.strptime(value, "%Y-%m-%d").strftime("%Y%m%d")
    except Exception:
        return value.replace("-", "")
