# Provider Fallback Chain

ChinaDataSourceManager tries providers in a fixed priority order per data type:

| Data type | Priority order |
|---|---|
| market_data | akshare → baostock → tushare |
| company_info | akshare → tushare → baostock |
| financial_info | tushare → akshare → baostock |
| news_events | akshare → tushare |

## Provider details

| Provider | Library | Requires API key? |
|---|---|---|
| akshare | `akshare` | No |
| baostock | `baostock` | No |
| tushare | `tushare` | `TUSHARE_TOKEN` (set via env var) |

If all providers fail, the result status is `unavailable` with attempt details for each provider.
