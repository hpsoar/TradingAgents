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

| User says | Script command |
|---|---|
| "show me all decisions", "历史记录", "past analyses" | `list-all` |
| "what did we decide on NVDA", "NVDA 之前的分析" | `filter-ticker NVDA` |
| "show me pending entries", "pending" | `pending` |
| "show me reflections", "反思" | `list-all` (then look for reflection=yes) |
| "give me past context for NVDA" | `past-context NVDA` |
| "show recent failures" | `list-all` (then filter by rating) |

### Step 2 — Verify setup

```bash
test -f ~/.tradingagents/.setup_done && echo "STAMP_OK" || echo "STAMP_MISSING"
```

If `STAMP_MISSING`, route to `tradingagents-setup`. Stop.

If `STAMP_OK`, read project root:

```bash
PROJECT_DIR=$(cat ~/.tradingagents/.setup_done 2>/dev/null)
```

### Step 3 — Query the memory log

All commands run from the project root:

```bash
cd "$PROJECT_DIR"
```

**All entries — summary:**
```bash
python skills/tradingagents-memory-review/scripts/review.py list-all
```

**Filter by ticker:**
```bash
python skills/tradingagents-memory-review/scripts/review.py filter-ticker NVDA
```

**Pending entries (no outcome data yet):**
```bash
python skills/tradingagents-memory-review/scripts/review.py pending
```

**Past context (formatted for prompt injection before running a new analysis):**
```bash
python skills/tradingagents-memory-review/scripts/review.py past-context NVDA 5 3
```

**Raw file read (fallback when Python import fails):**
```bash
cat ~/.tradingagents/memory/trading_memory.md 2>/dev/null || echo "Memory log not found."
```

### Step 4 — Report

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
- `review.py` exits with MEMORY_IMPORT_FAILED — route to setup.

## References

- `references/memory-commands.md` — full Python query examples
- `references/entry-format.md` — memory log entry tag format and fields
