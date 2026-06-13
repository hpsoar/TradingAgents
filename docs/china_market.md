# China Market Data Extension

`china_market` adds China A-share data access while keeping TradingAgents'
existing analysis flow intact.  The package is isolated so forked projects can
merge upstream TradingAgents updates with a small conflict surface.

## Install

Core TradingAgents does not install China market providers by default.

```bash
pip install ".[china]"
```

`TUSHARE_TOKEN` is optional.  Without it, Tushare is skipped and the extension
falls back to AkShare and BaoStock where possible.

## Scope

The first version targets basic analysis data preparation:

- Daily OHLCV market data.
- Basic company information.
- Core financial information.
- News and announcement-like events when available.

It does not add new analysts, change graph flow, change trading strategy, or
support minute bars, realtime order books, funds, futures, or Hong Kong stocks.

## Routing

TradingAgents continues using its existing `route_to_vendor` flow.  A thin
adapter checks whether the symbol is an A-share.  Non-A-share symbols keep the
existing vendor path.

Supported A-share inputs include:

- `600519.SH`
- `000001.SZ`
- `sh600519`
- `sz000001`
- common six-digit A-share codes such as `600519` and `300750`

Explicit non-A-share inputs such as `AAPL`, `TSLA`, `0700.HK`, and `9988.HK`
are left untouched.

## Provider Priority

Default provider fallback:

- Market data: AkShare, BaoStock, Tushare when configured.
- Company info: AkShare, Tushare when configured, BaoStock.
- Financial info: Tushare when configured, AkShare, BaoStock.
- News/events: AkShare, Tushare when configured and permitted.

Returned text includes source attempts and missing-data notes so downstream
agents can report data gaps instead of inventing unavailable facts.

## Testing

Default tests should mock provider responses and avoid live network calls.
Live AkShare/Tushare/BaoStock checks should stay as optional smoke tests.
