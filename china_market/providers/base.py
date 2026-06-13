"""Base provider contract for isolated China market data sources."""

from __future__ import annotations

from china_market.models import DataResult
from china_market.symbols import NormalizedSymbol


class BaseChinaProvider:
    name = "base"

    def is_available(self) -> bool:
        return False

    def get_market_data(
        self, symbol: NormalizedSymbol, start_date: str, end_date: str
    ) -> DataResult:
        return self._not_available("market_data", symbol)

    def get_company_info(self, symbol: NormalizedSymbol) -> DataResult:
        return self._not_available("company_info", symbol)

    def get_financial_info(self, symbol: NormalizedSymbol) -> DataResult:
        return self._not_available("financial_info", symbol)

    def get_news_events(
        self, symbol: NormalizedSymbol, start_date: str | None = None,
        end_date: str | None = None, limit: int = 10
    ) -> DataResult:
        return self._not_available("news_events", symbol)

    def _not_available(self, kind: str, symbol: NormalizedSymbol) -> DataResult:
        return DataResult.unavailable(
            kind=kind,
            symbol=symbol.canonical,
            message=f"{self.name} provider is not available.",
        )
