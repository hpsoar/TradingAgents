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

Run analysis commands from the fixed TradingAgents project directory: `~/.tradingagents/source/TradingAgents`.

```bash
cd ~/.tradingagents/source/TradingAgents
test -d tradingagents
test -d cli
test -f extensions/run/cli.py
python -c "import tradingagents; import cli; import extensions.run.cli"
python -m extensions.run.cli --help
```

- If `cd ~/.tradingagents/source/TradingAgents` fails, use `tradingagents-setup` to create or clone the project there.
- If any `test` command fails, use `tradingagents-setup` to repair the fixed project directory.
- If the import command fails with `ModuleNotFoundError`, use `tradingagents-setup` to install dependencies.
- If `python -m extensions.run.cli --help` fails, use `tradingagents-setup` to repair the runner environment.

### 3. Verify run configuration

- Read `.env` and the current process environment.
- Required setting: `TRADINGAGENTS_LLM_PROVIDER`.
- Useful settings: `TRADINGAGENTS_QUICK_THINK_LLM`, `TRADINGAGENTS_DEEP_THINK_LLM`, `TRADINGAGENTS_LLM_BACKEND_URL`, `TRADINGAGENTS_OUTPUT_LANGUAGE`, `TRADINGAGENTS_MAX_DEBATE_ROUNDS`, `TRADINGAGENTS_MAX_RISK_ROUNDS`, `TRADINGAGENTS_CHECKPOINT_ENABLED`.
- If provider or model settings are missing or wrong, use `tradingagents-llm`.
- Map the provider to its credential env var using `references/provider-env.md`; `ollama` requires no API key.
- Check only whether the credential env var is present. Never print the key value.
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
- Provider credential mapping: `references/provider-env.md`
