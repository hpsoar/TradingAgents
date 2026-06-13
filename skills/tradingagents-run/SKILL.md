---
name: tradingagents-run
description: Run or inspect TradingAgents analysis. Use when the user asks to analyze a ticker, adjust analysis options, batch runs, or summarize saved results.
---

# TradingAgents Run

Run or inspect TradingAgents analysis from a ready local environment.

## Use When

- Analyze a ticker.
- Batch-run tickers.
- Choose analysts, research depth, report language, date, or asset type.
- Inspect or summarize prior TradingAgents outputs.

## Execution Process

### 1. Choose run mode

- If the user asks to summarize existing output, read the provided `result.json` or report files and skip execution.
- If the user asks for one analysis, create one task JSON.
- If the user asks for a batch, create one task JSON per symbol/date pair and run them sequentially.

### 2. Check readiness

```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py --check-only
```

- If the setup script reports setup problems, use `tradingagents-setup` and stop this run.
- If the setup script reports missing credentials, report the exact env var and stop.
- Continue only when check-only passes.

### 3. Apply requested config changes

- If the user requested provider, model, endpoint, or credential-setting changes, use `tradingagents-llm` before creating the task.
- Do not edit `.env` in this skill.
- Before execution, confirm the user approves external data calls and LLM token usage.

### 4. Create the task JSON

- Required fields: `symbol`, `analysis_date`, `asset_type`, `analysts`, `research_depth`, `output_language`, `output_dir`.
- Reject future `analysis_date` values.
- Allow only these analysts: `market`, `social`, `news`, `fundamentals`.
- Default `research_depth` to `1`.
- Write `task.json` under the selected output directory.

### 5. Run the task

```bash
cd ~/.tradingagents/source/TradingAgents
python -m extensions.run.cli run --task PATH_TO_TASK_JSON --result-file PATH_TO_RESULT_JSON
```

- For batches, run one task at a time and keep result files separate.

### 6. Read result

- Read `result.json`.
- Use the `artifacts` field to find report files.
- Report status, decision, result path, report paths, summary, and next action.
## Allowed Writes

- Task JSON under the selected output directory.
- Result JSON and generated report artifacts from a run.
- Checkpoints only when requested or enabled in the task.

Do not write credentials, provider source files, model catalogs, validators, or unrelated repo files.

## Inputs

- `symbol`: ticker with suffix when needed, such as `NVDA`, `0700.HK`, `600519.SS`, or `BTC-USD`.
- `analysis_date`: `YYYY-MM-DD`; never use a future date.
- `asset_type`: usually `stock`; use `crypto` for crypto symbols.
- `analysts`: subset of `market`, `social`, `news`, `fundamentals`; omit for all four.
- `research_depth`: integer at least `1`; default to `1`.
- `output_language`: report language, such as `English` or `Chinese`.

## Stop Conditions

- Future analysis date.
- Unsupported analyst name.
- Missing provider selection or provider credential.
- User has not approved external API calls and LLM token usage.
- Output directory is unwritable.

## Report Format

```text
Run status: success | failed | blocked
Symbol:
Analysis date:
Provider:
Decision:
Result file:
Report files:
Summary:
Next step:
```

## References

- Task JSON and runner commands: `references/task-runner.md`
- Interactive CLI and Python API alternatives: `references/run-modes.md`
- Output locations and result fields: `references/outputs.md`
