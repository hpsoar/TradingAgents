"""Provider manager and fallback chains for China A-share data."""

from __future__ import annotations

from collections.abc import Iterable
from concurrent.futures import ThreadPoolExecutor, TimeoutError as _FutureTimeoutError
from datetime import datetime, timedelta

from china_market.config import get_config as _get_china_config
from china_market.formatters import format_result
from china_market.models import DataResult, SourceAttempt
from china_market.providers.akshare_provider import AkShareProvider
from china_market.providers.baostock_provider import BaoStockProvider
from china_market.providers.base import BaseChinaProvider
from china_market.providers.tushare_provider import TushareProvider
from china_market.symbols import normalize_symbol


class ChinaDataSourceManager:
    """Route A-share data requests to optional providers with fallback."""

    def __init__(self, providers: Iterable[BaseChinaProvider] | None = None, timeout: int | None = None):
        self.providers = list(providers) if providers is not None else [
            AkShareProvider(),
            TushareProvider(),
            BaoStockProvider(),
        ]
        self._timeout = timeout if timeout is not None else _get_china_config().request_timeout

    def get_market_data(self, symbol: str, start_date: str, end_date: str) -> str:
        result = self._call_chain(
            "market_data",
            ("akshare", "baostock", "tushare"),
            "get_market_data",
            symbol,
            start_date,
            end_date,
        )
        return format_result(result)

    def get_company_info(self, symbol: str) -> str:
        result = self._call_chain(
            "company_info",
            ("akshare", "tushare", "baostock"),
            "get_company_info",
            symbol,
        )
        return format_result(result)

    def get_financial_info(self, symbol: str) -> str:
        result = self._call_chain(
            "financial_info",
            ("tushare", "akshare", "baostock"),
            "get_financial_info",
            symbol,
        )
        return format_result(result)

    def get_news_events(
        self, symbol: str, start_date: str | None = None,
        end_date: str | None = None, limit: int = 10
    ) -> str:
        result = self._call_chain(
            "news_events",
            ("akshare", "tushare"),
            "get_news_events",
            symbol,
            start_date,
            end_date,
            limit,
        )
        return format_result(result)

    def get_indicators(
        self, symbol: str, indicator: str, curr_date: str, look_back_days: int = 30
    ) -> str:
        return (
            self.get_market_data(symbol, _lookback_placeholder(curr_date, look_back_days), curr_date)
            + "\n\n"
            + f"Indicator request: {indicator}. Use the OHLCV rows above for technical analysis; "
            + "china_market does not change TradingAgents indicator strategy."
        )

    def _call_chain(
        self,
        kind: str,
        provider_order: tuple[str, ...],
        method_name: str,
        raw_symbol: str,
        *args,
    ) -> DataResult:
        symbol = normalize_symbol(raw_symbol)
        if symbol is None:
            return DataResult.unavailable(
                kind,
                raw_symbol,
                "Input is not recognized as an A-share symbol.",
            )

        providers = {provider.name: provider for provider in self.providers}
        attempts: list[SourceAttempt] = []
        for provider_name in provider_order:
            provider = providers.get(provider_name)
            if provider is None:
                attempts.append(SourceAttempt(provider_name, "skipped", "provider not configured"))
                continue
            pool: ThreadPoolExecutor | None = None
            try:
                pool = ThreadPoolExecutor(max_workers=1)
                future = pool.submit(getattr(provider, method_name), symbol, *args)
                result = future.result(timeout=self._timeout)
            except _FutureTimeoutError:
                attempts.append(SourceAttempt(provider.name, "timeout", f"timed out after {self._timeout}s"))
                if pool is not None:
                    pool.shutdown(wait=False)
                continue
            except Exception as exc:
                attempts.append(SourceAttempt(provider.name, "error", str(exc)))
                if pool is not None:
                    pool.shutdown(wait=False)
                continue
            finally:
                if pool is not None:
                    pool.shutdown(wait=False)

            attempts.append(SourceAttempt(provider.name, result.status, result.message))
            if result.usable:
                result.attempts = attempts
                return result

        return DataResult.unavailable(
            kind,
            symbol.canonical,
            "All China market providers failed or returned no usable data.",
            attempts=attempts,
        )


def _lookback_placeholder(curr_date: str, look_back_days: int) -> str:
    try:
        current = datetime.strptime(curr_date, "%Y-%m-%d").date()
        return (current - timedelta(days=look_back_days)).isoformat()
    except Exception:
        return curr_date
