import pytest

from tradingagents.dataflows import interface


@pytest.mark.unit
def test_a_share_symbols_route_to_china_market(monkeypatch):
    import china_market.adapters.tradingagents_adapter as adapter

    monkeypatch.setattr(adapter, "route_method", lambda method, *args, **kwargs: f"china:{method}:{args[0]}")

    assert interface.route_to_vendor("get_stock_data", "600519", "2026-01-01", "2026-01-02") == (
        "china:get_stock_data:600519"
    )


@pytest.mark.unit
def test_non_a_share_symbols_keep_existing_vendor_routing(monkeypatch):
    import china_market.adapters.tradingagents_adapter as adapter

    called = {"china": False}

    def fail_if_called(method, *args, **kwargs):
        called["china"] = True
        raise AssertionError("china_market should not handle non-A-share symbols")

    monkeypatch.setattr(adapter, "route_method", fail_if_called)
    monkeypatch.setattr(interface, "get_vendor", lambda category, method=None: "fake")
    monkeypatch.setitem(
        interface.VENDOR_METHODS["get_stock_data"],
        "fake",
        lambda symbol, start_date, end_date: f"existing:{symbol}",
    )

    assert interface.route_to_vendor("get_stock_data", "AAPL", "2026-01-01", "2026-01-02") == "existing:AAPL"
    assert called["china"] is False
