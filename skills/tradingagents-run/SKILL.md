---
name: tradingagents-run
description: "Execute TradingAgents multi-agent analysis for one or more ticker/date pairs. Use when: the user says 'analyze', 'run', 'research', 'evaluate' a stock/crypto/ticker; or says 'batch' with multiple tickers; or asks to review or summarize past run output in result.json. Do NOT use for setup, install, or .env configuration — route those to tradingagents-setup or tradingagents-config."
allowed-tools: Bash(python *), Bash(cat *), Bash(test *), Bash(ls *), Bash(mkdir *)
---

# TradingAgents Run

Execute TradingAgents core analysis and return a trading decision.

## Prerequisites

`tradingagents-setup` must have completed successfully before using this skill.

## Decision Tree

### Step 1 — Determine what the user wants

| Pattern | Action |
|---|---|
| "analyze NVDA", "run AAPL" etc. | Single analysis, go to Step 2 |
| "analyze NVDA and AAPL", "batch: 0700.HK, 600519.SS" | Batch, go to Step 2 but repeat for each |
| "show me past results", "review output", "what did we get for NVDA" | Go to Step 8 (review only) |

### Step 2 — Collect required inputs

For every analysis, the user MUST provide:
- `symbol` — ticker symbol. Reject values containing `/`, `..`, or whitespace.

Ask the user if not already provided:
- `analysis_date` — `YYYY-MM-DD`. Reject dates after today. If user says "yesterday" or "last week", compute the date.
- `output_dir` — where to write files. If user does not specify, use `runs/{symbol}-{analysis_date}`.

Optional (use defaults if not specified):
| Field | Default | Notes |
|---|---|---|
| `asset_type` | `stock` | Use `crypto` for BTC-USD, ETH-USD etc. |
| `analysts` | all four | Comma-separated from: market, social, news, fundamentals |
| `research_depth` | 1 | Integer 1-10 |
| `output_language` | English | English or Chinese |
| `task_id` | `{symbol}-{analysis_date}` | Auto-generated, override only if user provides one |
| `checkpoint_enabled` | false | Set true for long-running analyses that might crash |

Stop and do not proceed if symbol or analysis_date is missing.

### Step 3 — Verify setup is complete

Check the stamp file and module import:

```bash
test -f ~/.tradingagents/.setup_done && echo "STAMP_OK" || echo "STAMP_MISSING"
```

If `STAMP_MISSING`, tell the user setup has not been completed and route to `tradingagents-setup`. Stop.

If `STAMP_OK`, read the project root from the stamp and verify the module:

```bash
PROJECT_DIR=$(cat ~/.tradingagents/.setup_done)
cd "$PROJECT_DIR"
python -c "import tradingagents; print('IMPORT_OK')" 2>&1
```

If import fails, report that setup is broken and route to `tradingagents-setup`. Stop.

If both pass, the project root is `$PROJECT_DIR`. All subsequent commands run from there.

### Step 4 — Confirm with user

```text
Planned analysis:
  Symbol: NVDA
  Date: 2024-05-10
  Analysts: market, social, news, fundamentals
  Depth: 1
  Language: English

This will call LLM APIs and consume tokens. Proceed? (yes/no)
```

If user says no, stop. If user says yes, continue.

### Step 5 — Create task JSON

Create the output directory:

```bash
mkdir -p runs/nvda-2024-05-10
```

Write the task JSON to `runs/nvda-2024-05-10/task.json`:

```json
{
  "schema_version": "1.0",
  "task_id": "nvda-2024-05-10",
  "symbol": "NVDA",
  "analysis_date": "2024-05-10",
  "asset_type": "stock",
  "analysts": ["market", "social", "news", "fundamentals"],
  "research_depth": 1,
  "output_language": "English",
  "output_dir": "runs/nvda-2024-05-10",
  "checkpoint_enabled": false
}
```

Rules:
- `task_id` — use user-provided or auto-generated
- `symbol` — uppercase it
- `analysts` — if user said "skip news", omit it; if user said "only market", use `["market"]`
- `research_depth` — clamp to 1-10
- `output_dir` — must be an absolute or relative path from the project root

### Step 6 — Run the analysis

```bash
python -m extensions.run.cli run \
  --task runs/nvda-2024-05-10/task.json \
  --result-file runs/nvda-2024-05-10/result.json 2>&1
```

| Exit code | stderr pattern | Meaning | Action |
|---|---|---|---|
| 0 | `Result written to: ...` | Success | Go to Step 7 |
| 1 | `validation_error:` | Bad inputs | Report the error, stop |
| 1 | `configuration_error:` | Credential/model issue | Route to `tradingagents-config`, stop |
| 1 | `data_unavailable:` | Vendor/ticker issue | Report the error, stop |
| 1 | `model_error:` | LLM call failed | Report the error, stop |
| 1 | `INTERNAL_ERROR:` | Bug | Report the error, stop |

### Step 7 — Read and report results

```bash
cat runs/nvda-2024-05-10/result.json
```

Extract and report:

```
Run status: success | <error_code>
Symbol: NVDA
Analysis date: 2024-05-10
Decision: strong_buy | buy | hold | sell | strong_sell
Result file: runs/nvda-2024-05-10/result.json
Summary: <2-3 sentences>
Next step:
```

For batches, repeat Steps 5-7 per ticker, reporting each separately.

### Step 8 — Review past results

```bash
ls ~/.tradingagents/source/TradingAgents/runs/ 2>/dev/null || echo "no runs"
```

If user specifies a ticker/date, read that `result.json`. Otherwise list all available.

```
Run status: success | <error_code>
Symbol: NVDA
Analysis date: 2024-05-10
Decision: buy
Result file: ~/.tradingagents/source/TradingAgents/runs/nvda-2024-05-10/result.json
```

## Allowed Writes

- Task JSON and result JSON under each run output directory.
- Checkpoint SQLite databases (only when `checkpoint_enabled`).

Do NOT write to `.env`, source code, model catalogs, or credentials.

## Stop Conditions

- `symbol` contains `/`, `..`, or whitespace.
- `analysis_date` is after today.
- `analysts` contains a name not in `market`, `social`, `news`, `fundamentals`.
- Setup stamp is missing or module import fails — route to setup.
- User has not approved API call.

## References

- `references/task-runner.md` — full task JSON schema and example
- `references/run-modes.md` — interactive CLI and Python API alternatives
- `references/outputs.md` — result format and failure categories
