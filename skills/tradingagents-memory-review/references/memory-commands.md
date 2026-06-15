# Memory Query Commands

## Load all entries
```python
from tradingagents.agents.utils.memory import TradingMemoryLog
log = TradingMemoryLog()
entries = log.load_entries()
for e in entries:
    print(e)
```

## Get pending entries
```python
pending = log.get_pending_entries()
```

## Get past context for prompt injection
```python
ctx = log.get_past_context("NVDA", n_same=5, n_cross=3)
```

## Entry fields
| Field | Type | Example |
|---|---|---|
| date | string | "2024-05-10" |
| ticker | string | "NVDA" |
| rating | string | "buy" |
| pending | bool | false |
| raw | string or None | "+8.2%" |
| alpha | string or None | "+3.1%" |
| holding | string or None | "30d" |
| decision | string | Full decision text |
| reflection | string or "" | Reflection text |
