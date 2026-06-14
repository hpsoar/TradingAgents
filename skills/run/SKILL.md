---
name: run
description: Execute TradingAgents analysis for one or more tickers. Use when the user asks to analyze a stock, batch-run tickers, or inspect past results.
---

# Run

Execute TradingAgents core analysis.

## Use When

- Analyze a single ticker on a specific date.
- Batch-run multiple tickers or dates.
- Review or summarize existing output files.
- The setup skill has already been run and the environment is ready.

## Execution Process

### 1. Determine mode

- If the user asks to review past output, read the `result.json` or report files and stop.
- If the user wants new analysis, proceed.

### 2. Check environment readiness

```bash
python skills/setup/scripts/setup_tradingagents.py --check-only
```

- If it reports anything other than `Setup check passed.`, route to `setup` and stop.
- If it reports a missing credential, tell the user which env var and stop.

### 3. Gather inputs

Required:
- `symbol` — ticker with exchange suffix when needed (e.g. `NVDA`, `0700.HK`, `600519.SS`, `BTC-USD`)
- `analysis_date` — `YYYY-MM-DD` format; reject future dates
- `output_dir` — where to write task and result files

Optional (with defaults):
- `task_id` — auto-generate from `{symbol}-{analysis_date}` if not provided
- `asset_type` — `stock` (default) or `crypto`
- `analysts` — subset of `market`, `social`, `news`, `fundamentals`; omit for all four
- `research_depth` — integer 1-10, default 1
- `output_language` — `English` (default) or `Chinese`
- `llm_provider` — override the provider for this run
- `deep_think_llm` — model for deep reasoning
- `quick_think_llm` — model for quick tasks
- `backend_url` — custom API endpoint
- `checkpoint_enabled` — enable resume on crash

### 4. Confirm the run

Before executing, confirm the user approves the LLM API calls and token usage.

### 5. Create task JSON

Write a task JSON matching this schema:

```json
{
  "schema_version": "1.0",
  "task_id": "nvda-2024-05-10",
  "symbol": "NVDA",
  "analysis_date": "2024-05-10",
  "asset_type": "stock",
  "analysts": ["market", "news", "fundamentals"],
  "research_depth": 1,
  "output_language": "English",
  "output_dir": "runs/nvda-2024-05-10",
  "llm_provider": "openai",
  "checkpoint_enabled": false
}
```

All fields except `analysts`, `llm_provider`, `deep_think_llm`, `quick_think_llm`, `backend_url`, `checkpoint_enabled` are passed to the schema.

The `output_dir` will be created if it does not exist.

### 6. Run the task

```bash
python -m extensions.run.cli run \
  --task runs/nvda-2024-05-10/task.json \
  --result-file runs/nvda-2024-05-10/result.json
```

For batches, run one task at a time and keep separate output directories.

### 7. Read result

Read `result.json`. Report:

- Status (`success` / error code)
- Final decision
- Result file path
- Report files in `artifacts`
- Short summary

## Allowed Writes

- Task JSON files under each output directory.
- Result JSON and generated report artifacts from a run.
- Checkpoint databases (only when `checkpoint_enabled` is set).

Do not write credentials, source files, model catalogs, or `.env` entries.

## Stop Conditions

- Future `analysis_date`.
- Unsupported analyst name.
- `/` or `..` in ticker symbol (path traversal).
- Setup check reports blocked or missing credentials.
- User has not approved API calls.
- `output_dir` is unwritable.

## Report Format

```
Run status: success | validation_error | configuration_error | data_unavailable | model_error | internal_error
Symbol: NVDA
Analysis date: 2024-05-10
Decision: strong_buy | buy | hold | sell | strong_sell
Result file: runs/nvda-2024-05-10/result.json
Report files: runs/nvda-2024-05-10/analysis/summary.md
Summary: ...
Next step:
```

## References

- Task JSON and runner commands: `references/task-runner.md`
- Interactive CLI and Python API alternatives: `references/run-modes.md`
- Output locations and result fields: `references/outputs.md`
