# Dataflows Architecture

## Routing logic

1. Check if `china_market` should handle (A-share symbol) — if yes, route there
2. Check `tool_vendors` for method-level override
3. Fall back to `data_vendors` category-level setting
4. Build fallback chain: primary vendors first, then all other available vendors
5. `AlphaVantageRateLimitError` triggers vendor fallback
6. `NoMarketDataError` is collected; if all vendors fail, return `NO_DATA_AVAILABLE`

## Configuration API

```python
from tradingagents.dataflows.config import set_config, get_config

# Read current config
cfg = get_config()

# Set category-level vendors
set_config({
    "data_vendors": {
        "core_stock_apis": "alpha_vantage",
        "technical_indicators": "yfinance",
        "fundamental_data": "yfinance",
        "news_data": "alpha_vantage",
    }
})

# Set tool-level override (takes precedence)
set_config({
    "tool_vendors": {
        "get_stock_data": "alpha_vantage",
    }
})

# Reset all tool overrides
set_config({"tool_vendors": {}})
```

## Important

- Changes are in-memory only and persist for the duration of the Python process.
- To make permanent changes, edit `DEFAULT_CONFIG` in `tradingagents/default_config.py` or set env vars.
- The `china_market` module auto-detects A-share symbols and is not configurable via data_vendors.
