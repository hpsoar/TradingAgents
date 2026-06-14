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

| User says | Data type | Script command |
|---|---|---|
| "股价", "行情", "price", "market data" for 600519 | Market data (OHLCV) | `market-data` |
| "公司信息", "company info" for 600519 | Company profile | `company-info` |
| "财务", "财报", "financials", "财务数据" for 600519 | Financial data | `financials` |
| "新闻", "news" for 600519 | News & events | `news` |
| "技术指标", "indicators", "技术分析" for 600519 | Technical indicators | `indicators` |

### Step 2 — Collect inputs

**Symbol resolution** — Accept any A-share format:
- Raw code: `600519`, `000001`
- With exchange: `600519.SH`, `000001.SZ`, `SH600519`, `SZ000001`
- Chinese names: resolve to code before passing to the module. If unknown, ask user for the 6-digit code.

Reject values containing `/`, `..`, or whitespace.

**Date parameters:**
- For `market-data` and `news`, both start_date and end_date are optional. Default: start=30 days ago, end=today. Do not ask.
- For `indicators`, curr_date defaults to today and lookback_days defaults to 30.

**News limit:** Default 10. Accept user override.

### Step 3 — Verify setup

```bash
test -f ~/.tradingagents/.setup_done && echo "STAMP_OK" || echo "STAMP_MISSING"
```

If `STAMP_MISSING`, route to `tradingagents-setup` with `--china-extra` flag.

If `STAMP_OK`, read the project root and verify china_market:

```bash
PROJECT_DIR=$(cat ~/.tradingagents/.setup_done)
cd "$PROJECT_DIR"
python skills/tradingagents-china-market/scripts/query.py verify
```

If output is `CHINA_OK`, proceed. If import fails (CHINA_IMPORT_FAILED), report that China extras are not installed and route to `tradingagents-setup --china-extra`. Stop.

### Step 4 — Run the query

All commands run from the project root (`$PROJECT_DIR`):

```bash
cd "$PROJECT_DIR"
```

Query templates by data type:

**Market data (OHLCV):**
```bash
python skills/tradingagents-china-market/scripts/query.py market-data 600519.SH 2024-05-01 2024-06-01
```

**Company info:**
```bash
python skills/tradingagents-china-market/scripts/query.py company-info 600519.SH
```

**Financial data:**
```bash
python skills/tradingagents-china-market/scripts/query.py financials 600519.SH
```

**News & events:**
```bash
python skills/tradingagents-china-market/scripts/query.py news 600519.SH 2024-05-01 2024-06-01 10
```

**Technical indicators:**
```bash
python skills/tradingagents-china-market/scripts/query.py indicators 600519.SH SMA_20 2024-06-01 30
```

Replace argument values with the collected inputs. Date defaults apply when omitted.

### Step 5 — Report results

```
Data type: market-data | company-info | financials | news | indicators
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
- `query.py verify` returns CHINA_IMPORT_FAILED — route to setup with `--china-extra`.
- Symbol is not recognized as a valid A-share format (6-digit code, SH/SZ exchange).
- Symbol contains `/`, `..`, or whitespace.

## References

- `references/china-commands.md` — example commands for each data type
- `references/provider-chain.md` — fallback logic among akshare/tushare/baostock
- `references/symbol-formats.md` — supported A-share symbol formats
