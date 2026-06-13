"""End-to-end smoke tests for China A-share data providers.

These tests hit real data sources and may fail due to network issues,
rate limits, or upstream API changes. They are NOT part of default CI.
Run manually with: uv run python3 -m pytest tests/test_china_market_e2e_smoke.py -v
"""

import sys

import pytest

from china_market.manager import ChinaDataSourceManager
from china_market.symbols import normalize_symbol


def _check_result_text(text: str, data_type: str, symbol: str) -> None:
    assert "China A-share data for" in text, f"Missing header in {data_type}"
    assert symbol in text, f"Expected symbol {symbol} not found in {data_type}"
    assert "status:" in text, f"Missing status in {data_type}"
    # If the overall status is unavailable, the message must explain why.
    if "status: unavailable" in text:
        assert "NO_DATA_AVAILABLE" in text or "Cannot" in text, (
            f"Unavailable data should explain why: {text[:200]}"
        )


@pytest.mark.smoke
def test_e2e_market_data_akshare():
    """Fetch daily market data for a well-known A-share stock via AkShare."""
    manager = ChinaDataSourceManager()
    text = manager.get_market_data("600519", "2025-01-02", "2025-01-10")
    _check_result_text(text, "market_data", "600519.SH")
    assert "status: success" in text or "status: partial" in text, (
        f"Expected success/partial, got:\n{text[:300]}"
    )


@pytest.mark.smoke
def test_e2e_company_info_akshare():
    """Fetch company info for Kweichow Moutai via AkShare."""
    manager = ChinaDataSourceManager()
    text = manager.get_company_info("600519")
    _check_result_text(text, "company_info", "600519.SH")
    assert "status: success" in text or "status: partial" in text, (
        f"Expected success/partial, got:\n{text[:300]}"
    )


@pytest.mark.smoke
def test_e2e_news_events_akshare():
    """Fetch recent news for 600519 via AkShare."""
    manager = ChinaDataSourceManager()
    text = manager.get_news_events("600519.SH", limit=5)
    _check_result_text(text, "news_events", "600519.SH")
    # News may be partial or unavailable; just verify diagnostics
    assert "source_attempts:" in text, f"Missing provider chain info:\n{text[:300]}"


@pytest.mark.smoke
def test_e2e_shenzhen_market_data():
    """Fetch market data for a Shenzhen-listed A-share (300750.SZ - CATL)."""
    manager = ChinaDataSourceManager()
    text = manager.get_market_data("300750", "2025-01-02", "2025-01-10")
    _check_result_text(text, "market_data", "300750.SZ")
    assert "status: success" in text or "status: partial" in text, (
        f"Expected success/partial, got:\n{text[:300]}"
    )


@pytest.mark.smoke
def test_e2e_financial_info_akshare():
    """Fetch financial summary via AkShare (may be partial)."""
    manager = ChinaDataSourceManager()
    text = manager.get_financial_info("600519")
    _check_result_text(text, "financial_info", "600519.SH")
    # Financial info may be partial depending on data source availability


@pytest.mark.smoke
def test_e2e_non_a_share_untouched():
    """Verify non-A-share symbols are rejected by china_market."""
    manager = ChinaDataSourceManager()
    text = manager.get_market_data("AAPL", "2025-01-01", "2025-01-10")
    assert "not recognized as an A-share symbol" in text
    assert "status: unavailable" in text


@pytest.mark.smoke
def test_e2e_symbol_normalization():
    """Verify real symbol normalization works on the full pipeline."""
    cases = [
        ("600519", "600519.SH"),
        ("sh600519", "600519.SH"),
        ("000001.SZ", "000001.SZ"),
        ("sz000001", "000001.SZ"),
    ]
    for raw, expected in cases:
        sym = normalize_symbol(raw)
        assert sym is not None, f"Failed to normalize {raw}"
        assert sym.canonical == expected, f"{raw} -> {sym.canonical}, expected {expected}"
