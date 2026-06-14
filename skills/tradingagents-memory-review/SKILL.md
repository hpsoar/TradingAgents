---
name: tradingagents-memory-review
description: "Query historical trading decisions and reflections from the TradingMemoryLog. Use when: the user asks 'what did we decide on NVDA last time', 'show me past analyses', 'what were the reflections on our last trade', 'any pending entries?', or wants past context before running a new analysis. Do NOT use for running new analysis — route that to tradingagents-run."
allowed-tools: Bash(python *), Bash(cat *), Bash(test *), Bash(ls *)
---

# TradingAgents Memory Review

Query the append-only memory log of past trading decisions and reflections.

## Prerequisites

`tradingagents-setup` must have completed successfully (the memory log path is created during setup).

## Decision Tree

### Step 1 — Determine what the user wants

| User says | Action |
|---|---|
| "show me all decisions", "历史记录", "past analyses" | List all entries |
| "what did we decide on NVDA", "NVDA 之前的分析" | Filter entries for a specific ticker |
| "show me pending entries", "pending" | Show entries not yet resolved with returns |
| "show me reflections", "反思" | Show entries that have a REFLECTION section |
| "give me past context for NVDA" | Get formatted context for prompt injection (same-ticker + cross-ticker lessons) |
| "show recent failures" | Filter by rating (sell/strong_sell) |

### Step 2 — Verify setup

```bash
test -f ~/.tradingagents/.setup_done && echo "STAMP_OK" || echo "STAMP_MISSING"
```

If `STAMP_MISSING`, route to `tradingagents-setup`. Stop.

Read project root:
```bash
PROJECT_DIR=$(cat ~/.tradingagents/.setup_done 2>/dev/null)
```

### Step 3 — Query the memory log

**All entries — summary:**
```bash
python -c "
import sys, json
sys.path.insert(0, '$PROJECT_DIR')
from tradingagents.agents.utils.memory import TradingMemoryLog
log = TradingMemoryLog()
entries = log.load_entries()
for e in entries:
    tag = f\"[{e['date']} | {e['ticker']} | {e['rating']} | {'pending' if e['pending'] else (e['raw'] or 'n/a')}]\"
    has_reflection = 'yes' if e.get('reflection') else 'no'
    print(f'{tag}  reflection={has_reflection}')
print(f'Total: {len(entries)} entries')
"
```

**Filter by ticker:**
```bash
python -c "
import sys
sys.path.insert(0, '$PROJECT_DIR')
from tradingagents.agents.utils.memory import TradingMemoryLog
log = TradingMemoryLog()
for e in log.load_entries():
    if e['ticker'] == 'NVDA':
        print(f\"[{e['date']} | {e['rating']} | {'pending' if e['pending'] else e['raw']}]\")
        print(f\"DECISION: {e['decision'][:200]}...\")
        if e.get('reflection'):
            print(f\"REFLECTION: {e['reflection']}\")
        print()
"
```

**Pending entries:**
```bash
python -c "
import sys
sys.path.insert(0, '$PROJECT_DIR')
from tradingagents.agents.utils.memory import TradingMemoryLog
log = TradingMemoryLog()
pending = log.get_pending_entries()
for e in pending:
    print(f\"[{e['date']} | {e['ticker']} | {e['rating']} | pending]\")
    print(f\"DECISION: {e['decision'][:300]}\")
    print()
print(f'Pending: {len(pending)} entries')
"
```

**Past context (formatted for prompt injection before running a new analysis):**
```bash
python -c "
import sys
sys.path.insert(0, '$PROJECT_DIR')
from tradingagents.agents.utils.memory import TradingMemoryLog
log = TradingMemoryLog()
ctx = log.get_past_context('NVDA', n_same=5, n_cross=3)
print(ctx if ctx else 'No past context available.')
"
```

**Raw file read (alternative when Python import fails):**
```bash
cat ~/.tradingagents/memory/trading_memory.md 2>/dev/null || echo "Memory log not found."
```

### Step 4 — Report

Format results clearly:

```
Memory log: ~/.tradingagents/memory/trading_memory.md
Total entries: 12
Pending: 2

Entries matching NVDA:

[2024-05-10 | NVDA | buy | +8.2% | +3.1% | 30d]
DECISION: Buy NVDA at $120.50...
REFLECTION: The thesis was correct...

[2024-04-15 | NVDA | hold | pending]
DECISION: Hold NVDA pending Q2 earnings...

Next step: Use tradingagents-run to run a new analysis, or tradingagents-memory-review with a different filter.
```

## Allowed Writes

None. This skill is read-only. Never modify the memory log file, `.env`, or source code.

## Stop Conditions

- Setup stamp is missing — route to setup.
- Memory log file does not exist (no analyses have been run yet) — report "No past decisions found."
- Python `tradingagents` module import fails — route to setup.

## References

- `references/memory-commands.md` — full Python query examples
- `references/entry-format.md` — memory log entry tag format and fields
