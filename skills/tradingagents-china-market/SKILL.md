---
name: tradingagents-china-market
description: "Query China A-share market data (market data, company info, financials, news, indicators) using the standalone china_market module. Use when: the user asks about a Chinese A-share stock (6-digit code like 600519, 600519.SH, SH600519) and wants price data, company info, financials, news, or technical indicators. Do NOT use for US/HK tickers — route those to other data sources."
allowed-tools: Bash(python *), Bash(cat *), Bash(test *), Bash(ls *)
---

# TradingAgents China A-Share Market

Query China A-share market data independently of the full analysis pipeline.

## Prerequisites

`tradingagents-setup` must have completed successfully. The china_market module is available only when the `--china-extra` flag was used during setup (i.e., `pip install tradingagents[china]` was run).

## Decision Tree

### Step 1 — Determine what data the user wants

| User says | Data type | Method |
|---|---|---|
| "股价", "行情", "price", "market data" for 600519 | Market data (OHLCV) | `get_market_data(symbol, start_date, end_date)` |
| "公司信息", "company info" for 600519 | Company profile | `get_company_info(symbol)` |
| "财务", "财报", "financials", "财务数据" for 600519 | Financial data | `get_financial_info(symbol)` |
| "新闻", "news" for 600519 | News & events | `get_news_events(symbol, start_date, end_date, limit)` |
| "技术指标", "indicators", "技术分析" for 600519 | Technical indicators | `get_indicators(symbol, indicator, curr_date, look_back_days)` |

### Step 2 — Collect inputs

**Symbol resolution** — Accept any A-share format:
- Raw code: `600519`, `000001`
- With exchange: `600519.SH`, `000001.SZ`, `SH600519`, `SZ000001`
- Chinese names: resolve to code before passing to the module. If unknown, ask user for the 6-digit code.

Reject values containing `/`, `..`, or whitespace.

**Date parameters:**
- For `get_market_data` and `get_news_events`, both `start_date` and `end_date` are required (YYYY-MM-DD).
- If user does not provide dates, default: `start_date` = 30 days ago, `end_date` = today. Do not ask.
- For `get_indicators`, `curr_date` defaults to today and `look_back_days` defaults to 30.

**News limit:** Default 10. Accept user override.

### Step 3 — Verify setup

```bash
test -f ~/.tradingagents/.setup_done && echo "STAMP_OK" || echo "STAMP_MISSING"
```

If `STAMP_MISSING`, route to `tradingagents-setup` with `--china-extra` flag.

If `STAMP_OK`, verify the china_market package:

```bash
PROJECT_DIR=$(cat ~/.tradingagents/.setup_done)
python -c "from china_market.manager import ChinaDataSourceManager; print('CHINA_OK')" 2>&1
```

If import fails, report that China extras are not installed and route to `tradingagents-setup --china-extra`. Stop.

### Step 4 — Run the query

All queries use `ChinaDataSourceManager` from the project root:

```bash
cd "$PROJECT_DIR"
python -c "
from china_market.manager import ChinaDataSourceManager
mgr = ChinaDataSourceManager()
print(mgr.get_market_data('600519.SH', '2024-05-01', '2024-06-01'))
"
```

Query templates by data type:

**Market data (OHLCV):**
```bash
python -c "
from china_market.manager import ChinaDataSourceManager
mgr = ChinaDataSourceManager()
print(mgr.get_market_data('SYMBOL', 'START_DATE', 'END_DATE'))
"
```

**Company info:**
```bash
python -c "
from china_market.manager import ChinaDataSourceManager
mgr = ChinaDataSourceManager()
print(mgr.get_company_info('SYMBOL'))
"
```

**Financial data:**
```bash
python -c "
from china_market.manager import ChinaDataSourceManager
mgr = ChinaDataSourceManager()
print(mgr.get_financial_info('SYMBOL'))
"
```

**News & events:**
```bash
python -c "
from china_market.manager import ChinaDataSourceManager
mgr = ChinaDataSourceManager()
print(mgr.get_news_events('SYMBOL', 'START_DATE', 'END_DATE', LIMIT))
"
```

**Technical indicators (returns OHLCV data + indicator request text):**
```bash
python -c "
from china_market.manager import ChinaDataSourceManager
mgr = ChinaDataSourceManager()
print(mgr.get_indicators('SYMBOL', 'INDICATOR_NAME', 'CURR_DATE', LOOKBACK_DAYS))
"
```

### Step 5 — Report results

For each query, display:

```
Data type: market_data | company_info | financials | news | indicators
Symbol: 600519.SH
Period: 2024-05-01 → 2024-06-01
Status: success | unavailable
Provider chain: akshare → tushare → baostock

<data output>

Next step: Run a full tradingagents analysis, or query another symbol/data type.
```

If status is `unavailable`, report which providers failed and suggest checking the ticker or data source availability.

## Allowed Writes

None. This skill is read-only — it queries data and displays results. Never write to `.env`, source code, or cache files.

## Stop Conditions

- Setup stamp is missing — route to setup.
- `china_market` module import fails — route to setup with `--china-extra`.
- Symbol is not recognized as a valid A-share format (6-digit code, SH/SZ exchange).
- Symbol contains `/`, `..`, or whitespace.

## References

- `references/china-commands.md` — example commands for each data type
- `references/provider-chain.md` — fallback logic among akshare/tushare/baostock
- `references/symbol-formats.md` — supported A-share symbol formats
