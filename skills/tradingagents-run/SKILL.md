---
name: tradingagents-run
description: Run TradingAgents financial analysis from an already configured local repository checkout, using the repo-only non-interactive task runner by default, then locate and summarize saved reports. Use when the user asks to analyze a ticker, choose analysts, set research depth/debate rounds, set report language, inspect prior outputs, or automate TradingAgents runs from an agent.
---

# TradingAgents Run

Run or inspect TradingAgents analysis from a configured local source checkout. Setup and LLM configuration are separate skills.

## Use When

- Analyze a ticker.
- Batch-run tickers.
- Choose analysts, research depth, report language, date, or asset type.
- Inspect or summarize prior TradingAgents outputs.

## Do Not Use When

- The repo is not installed or dependencies are missing; use `tradingagents-setup`.
- Provider/model/API key configuration is the main task; use `tradingagents-llm`.
- The user has not approved external API calls and LLM token usage for a real analysis.
- The task requires source-code changes.

## Default Flow

1. Check readiness: repo checkout, dependencies, provider selection, and credentials.
2. Validate inputs: symbol, non-future analysis date, asset type, analyst names, and research depth.
3. If setup or credentials are missing, stop or hand off to the appropriate skill.
4. Confirm external API calls and LLM token usage before running a real analysis.
5. Create a task JSON for the non-interactive runner.
6. Run `python -m extensions.run.cli run ...`.
7. Read `result.json` and locate generated report artifacts.
8. Report status, decision, output paths, and a short summary.

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
