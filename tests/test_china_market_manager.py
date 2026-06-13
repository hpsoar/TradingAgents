import pytest

from china_market.manager import ChinaDataSourceManager
from china_market.models import DataResult


class FakeProvider:
    def __init__(self, name, status, data=None, message=""):
        self.name = name
        self.status = status
        self.data = data
        self.message = message

    def get_market_data(self, symbol, start_date, end_date):
        return DataResult(
            kind="market_data",
            symbol=symbol.canonical,
            status=self.status,
            provider=self.name,
            data=self.data,
            message=self.message,
        )


@pytest.mark.unit
def test_manager_uses_first_successful_provider():
    manager = ChinaDataSourceManager(
        providers=[
            FakeProvider("akshare", "unavailable", None, "empty"),
            FakeProvider("baostock", "success", [{"date": "2026-01-01"}]),
            FakeProvider("tushare", "success", [{"date": "ignored"}]),
        ]
    )

    text = manager.get_market_data("600519", "2026-01-01", "2026-01-02")

    assert "source_used: baostock" in text
    assert "akshare:unavailable(empty)" in text
    assert "baostock:success" in text
    assert "2026-01-01" in text


@pytest.mark.unit
def test_manager_reports_all_provider_failures():
    manager = ChinaDataSourceManager(
        providers=[
            FakeProvider("akshare", "unavailable", None, "empty"),
            FakeProvider("baostock", "unavailable", None, "login failed"),
        ]
    )

    text = manager.get_market_data("000001.SZ", "2026-01-01", "2026-01-02")

    assert "status: unavailable" in text
    assert "All China market providers failed" in text
    assert "akshare:unavailable(empty)" in text
    assert "baostock:unavailable(login failed)" in text


@pytest.mark.unit
def test_manager_rejects_non_a_share_symbols():
    manager = ChinaDataSourceManager(providers=[])

    text = manager.get_market_data("AAPL", "2026-01-01", "2026-01-02")

    assert "status: unavailable" in text
    assert "not recognized as an A-share symbol" in text
