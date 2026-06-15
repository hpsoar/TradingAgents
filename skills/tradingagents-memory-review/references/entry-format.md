# Memory Log Entry Format

## Tag line format

### Pending entry
```
[2024-05-10 | NVDA | buy | pending]
```

### Resolved entry
```
[2024-05-10 | NVDA | buy | +8.2% | +3.1% | 30d]
```

| Position | Field | Description |
|---|---|---|
| 1 | date | Analysis date (YYYY-MM-DD) |
| 2 | ticker | Stock symbol |
| 3 | rating | strong_buy/buy/hold/sell/strong_sell |
| 4 | outcome | "pending" or raw return % |
| 5 | alpha | Alpha vs benchmark % (resolved only) |
| 6 | holding | Holding period in days (resolved only) |

## Body sections

```
DECISION:
<full trade decision text>

REFLECTION:
<2-4 sentence reflection>
```

Entries are delimited by `<!-- ENTRY_END -->`.
