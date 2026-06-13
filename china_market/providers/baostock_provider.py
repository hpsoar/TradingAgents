"""BaoStock provider for fallback A-share data."""

from __future__ import annotations

from typing import Any

from china_market.models import DataResult
from china_market.providers.base import BaseChinaProvider
from china_market.symbols import NormalizedSymbol


class BaoStockProvider(BaseChinaProvider):
    name = "baostock"

    def __init__(self):
        self._bs: Any | None = None
        self._import_error: Exception | None = None

    @property
    def bs(self):
        if self._bs is None and self._import_error is None:
            try:
                import baostock as bs
                self._bs = bs
            except Exception as exc:  # pragma: no cover - provider availability path
                self._import_error = exc
        return self._bs

    def is_available(self) -> bool:
        return self.bs is not None

    def get_market_data(
        self, symbol: NormalizedSymbol, start_date: str, end_date: str
    ) -> DataResult:
        if not self.is_available():
            return self._not_available("market_data", symbol)
        fields = "date,code,open,high,low,close,volume,amount"
        rows = self._query(
            lambda: self.bs.query_history_k_data_plus(
                symbol.baostock_symbol,
                fields,
                start_date=start_date,
                end_date=end_date,
                frequency="d",
                adjustflag="3",
            )
        )
        if not rows:
            return DataResult.unavailable(
                "market_data", symbol.canonical, "BaoStock returned no market rows."
            )
        return DataResult("market_data", symbol.canonical, "success", self.name, rows)

    def get_company_info(self, symbol: NormalizedSymbol) -> DataResult:
        if not self.is_available():
            return self._not_available("company_info", symbol)
        rows = self._query(lambda: self.bs.query_stock_basic(code=symbol.baostock_symbol))
        if not rows:
            return DataResult.unavailable(
                "company_info", symbol.canonical, "BaoStock returned no company info."
            )
        return DataResult("company_info", symbol.canonical, "success", self.name, rows)

    def get_financial_info(self, symbol: NormalizedSymbol) -> DataResult:
        if not self.is_available():
            return self._not_available("financial_info", symbol)
        rows = self._query(lambda: self.bs.query_profit_data(code=symbol.baostock_symbol))
        if not rows:
            return DataResult.unavailable(
                "financial_info", symbol.canonical, "BaoStock returned no profit data."
            )
        return DataResult("financial_info", symbol.canonical, "success", self.name, rows)

    def _query(self, make_query):
        lg = self.bs.login()
        if getattr(lg, "error_code", "0") != "0":
            raise RuntimeError(f"BaoStock login failed: {lg.error_msg}")
        try:
            rs = make_query()
            if getattr(rs, "error_code", "0") != "0":
                raise RuntimeError(f"BaoStock query failed: {rs.error_msg}")
            rows = []
            while rs.next():
                rows.append(dict(zip(rs.fields, rs.get_row_data())))
            return rows
        finally:
            self.bs.logout()
