---
name: tradingagents-vendor-config
description: "Configure data vendors for TradingAgents — switch between yfinance and Alpha Vantage per data category (stock data, technical indicators, fundamentals, news) or per individual tool. Use when: the user says 'switch data source', 'use Alpha Vantage', 'change data vendor', 'set vendor for news', or tradingagents-run reports data_unavailable errors. Do NOT use for LLM provider changes — route those to tradingagents-config."
allowed-tools: Bash(python *), Bash(cat *), Bash(grep *), Bash(echo *), Bash(sed *), Bash(test *)
---

# TradingAgents Vendor Config

Configure which data provider TradingAgents uses for stock data, technical indicators, fundamentals, and news.

## Prerequisites

`tradingagents-setup` must have completed successfully.

## How Data Vendor Configuration Works

The vendor system has two levels:

1. **Category-level** (`data_vendors`) — sets the default vendor for all tools in a category:
   - `core_stock_apis` — stock price/volume data
   - `technical_indicators` — technical analysis indicators
   - `fundamental_data` — balance sheet, cash flow, income statement
   - `news_data` — ticker news, global news, insider transactions

2. **Tool-level** (`tool_vendors`) — overrides the category default for a specific tool function

Available vendors: `yfinance` (default), `alpha_vantage` (requires `ALPHA_VANTAGE_API_KEY`).

## Decision Tree

### Step 1 — Determine what the user wants

| User says | Script command |
|---|---|
| "switch to Alpha Vantage", "use Alpha Vantage for everything" | `set-all alpha_vantage` |
| "use yfinance for news, Alpha Vantage for stocks" | `set-category core_stock_apis alpha_vantage` |
| "use Alpha Vantage only for get_stock_data" | `set-tool get_stock_data alpha_vantage` |
| "show current vendor config", "当前数据供应商配置" | `show` |
| "reset to yfinance defaults" | `reset` |

### Step 2 — Verify setup

```bash
test -f ~/.tradingagents/.setup_done && echo "STAMP_OK" || echo "STAMP_MISSING"
```

If `STAMP_MISSING`, route to `tradingagents-setup`. Stop.

If `STAMP_OK`, read project root:

```bash
PROJECT_DIR=$(cat ~/.tradingagents/.setup_done 2>/dev/null)
```

### Step 3 — Read current configuration

```bash
cd "$PROJECT_DIR"
python skills/tradingagents-vendor-config/scripts/config.py show
```

### Step 4 — Validate requested changes

Supported vendor names:
| Vendor | Categories | Requires |
|---|---|---|
| `yfinance` | All four categories | Nothing extra |
| `alpha_vantage` | All four categories | `ALPHA_VANTAGE_API_KEY` in `.env` |

Supported category keys:
- `core_stock_apis`
- `technical_indicators`
- `fundamental_data`
- `news_data`

Stop if user asks for an unsupported vendor name or category key.

### Step 5 — Apply changes

All commands run from the project root:

```bash
cd "$PROJECT_DIR"
```

**Set all categories to Alpha Vantage:**
```bash
python skills/tradingagents-vendor-config/scripts/config.py set-all alpha_vantage
```

**Partial category change (e.g., only news):**
```bash
python skills/tradingagents-vendor-config/scripts/config.py set-category news_data alpha_vantage
```

**Single tool override:**
```bash
python skills/tradingagents-vendor-config/scripts/config.py set-tool get_stock_data alpha_vantage
```

**Reset to yfinance defaults:**
```bash
python skills/tradingagents-vendor-config/scripts/config.py reset
```

### Step 6 — Verify the change

```bash
python skills/tradingagents-vendor-config/scripts/config.py verify
```

Confirm the displayed values match the user's request.

### Step 7 — Check credentials (for alpha_vantage)

If switching to `alpha_vantage`:

```bash
python skills/tradingagents-vendor-config/scripts/config.py check-cred alpha_vantage
```

If missing, report: "Alpha Vantage requires `ALPHA_VANTAGE_API_KEY` in `.env`. Please add it or route to tradingagents-config."

### Step 8 — Report

```
Vendor config status: updated | unchanged
Previous: yfinance (all categories)
Current:
  core_stock_apis: alpha_vantage
  technical_indicators: alpha_vantage
  fundamental_data: alpha_vantage
  news_data: alpha_vantage
  tool_vendors: (none)
Required key: ALPHA_VANTAGE_API_KEY
Key status: present | missing
Note: Changes apply in-memory. Run a new analysis to verify.
```

## Allowed Writes

- In-memory config only (via `set_config()`). This skill does NOT write to `.env` or source files.

## Stop Conditions

- Setup stamp is missing — route to setup first.
- Vendor name is not `yfinance` or `alpha_vantage`.
- Category key is not one of the four supported categories.
- User provides an API key in chat — tell them to set it in `.env` manually.

## References

- `references/vendor-list.md` — full vendor/category matrix
- `references/dataflows-architecture.md` — how vendor routing works
- `references/env-keys.md` — credential env vars for each vendor
