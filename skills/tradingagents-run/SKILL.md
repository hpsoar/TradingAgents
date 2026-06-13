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

### 1. Decide whether to run or inspect

- New ticker analysis: create and run a task JSON.
- Existing result summary: read existing `result.json` or report files only; do not start a new run.
- Batch analysis: create one task directory per symbol/date pair and run them one by one.

### 2. Verify the environment can run an analysis

Use the setup helper as the readiness gate:

```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py --check-only
```

- If the helper reports a missing or invalid project directory, missing dependencies, failed imports, missing `.env`, missing data dirs, or install problems, use `tradingagents-setup` first.
- If the helper reports missing credentials only, stop and report the exact env var; do not run analysis.
- Continue only when the helper reports the fixed project directory, env file, data directories, install/import check, provider, and credential status as ready.

### 3. Confirm run configuration

- Read `.env` in `~/.tradingagents/source/TradingAgents` and the current process environment.
- Review the effective provider, quick model, deep model, backend URL, output language, debate rounds, risk rounds, and checkpoint flag.
- If the user requested provider/model/endpoint changes or the effective values are wrong, use `tradingagents-llm`.
- Do not edit `.env` from this skill.
- Stop before any real analysis unless the user has approved external data calls and LLM token usage.

### 4. Validate task inputs

- Validate `symbol`, `analysis_date`, `asset_type`, `analysts`, `research_depth`, `output_language`, and `output_dir`.
- Reject future dates.
- Allowed analysts: `market`, `social`, `news`, `fundamentals`.
- Default `research_depth` to `1`.
- Use an output directory that includes symbol and analysis date.

### 5. Run and inspect output

- Write `task.json` under the selected output directory.
- Run:

```bash
cd ~/.tradingagents/source/TradingAgents
python -m extensions.run.cli run --task PATH_TO_TASK_JSON --result-file PATH_TO_RESULT_JSON
```

- Read `result.json`.
- Locate report artifacts from the `artifacts` field in `result.json`.
- Report success, failure, or blocked status with the result path and next action.

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
