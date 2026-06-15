# A-Share Symbol Formats

The `normalize_symbol()` function in `china_market/symbols.py` accepts:

| Format | Example | Notes |
|---|---|---|
| Six-digit code only | `600519` | Exchange inferred from prefix (600xxx/601xxx/... = SH, 000xxx/300xxx/... = SZ) |
| SH/SZ prefix | `SH600519`, `SZ000001` | Explicit exchange prefix |
| Canonical | `600519.SH`, `000001.SZ` | Code.exchange format |
| Prefix dot | `SH.600519`, `SZ.000001` | Dot-separated prefix |

## Exchange inference

| Prefix range | Exchange |
|---|---|
| 600, 601, 603, 605, 688, 900 | SH (Shanghai) |
| 000, 001, 002, 003, 300, 301, 200 | SZ (Shenzhen) |

## Rejected formats

- `.HK` or `.US` suffixes (not A-share)
- Non-numeric or short codes
- Symbols containing `/`, `..`, or whitespace
