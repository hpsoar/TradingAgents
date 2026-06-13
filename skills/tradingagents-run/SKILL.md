---
name: tradingagents-run
description: Run TradingAgents financial analysis from an already configured local repository checkout, using the interactive CLI, the repo-only non-interactive task runner, or the Python API, then locate and summarize saved reports. Use when the user asks to analyze a ticker, choose analysts, set research depth/debate rounds, set report language, inspect prior outputs, or automate TradingAgents runs from an agent.
---

# TradingAgents Run

Use this skill only after the local repo has been set up. For environment setup or missing dependencies, use `tradingagents-setup` first.

## User Intents

Use this skill when the user says things like:

- "Analyze NVDA."
- "Run TradingAgents for 600519.SH in Chinese."
- "Use only market/news/fundamentals analysts."
- "Summarize the last TradingAgents result."
- "Batch-run these tickers."

For a run request, the agent owns the end-to-end workflow. The user should not need to manually call setup first.

## Scope

Primary use case: run an analysis in a configured TradingAgents repo.

The non-interactive task runner requires a repo checkout because it lives under `extensions/run`. It is not available from package-only installation.

## Inputs

- `symbol`: ticker with suffix when needed: `NVDA`, `0700.HK`, `600519.SS`, `BTC-USD`.
- `analysis_date`: `YYYY-MM-DD`; do not use a future date.
- `asset_type`: usually `stock`; use `crypto` for crypto symbols.
- `analysts`: subset of `market`, `social`, `news`, `fundamentals`; omit for all four.
- `research_depth`: integer debate depth; default to `1` unless the user asks for deeper research.
- `output_language`: report language, such as `English` or `Chinese`.
- Model/provider settings and API keys. Prefer environment variables for repeatable agent runs.

Before running a real analysis, confirm the user accepts external API calls and LLM token usage.

## Recommended Automation Flow

1. Check setup readiness:
   - If the current workspace is not a configured TradingAgents repo, follow `tradingagents-setup` first.
   - If dependencies are missing, follow `tradingagents-setup` first.
   - If provider credentials are missing, stop and tell the user which env var to add. Do not run analysis.
2. Validate inputs before creating a task:
   - `analysis_date` is not in the future.
   - `analysts` contains only supported analyst names.
   - `research_depth` is at least `1`; use `1` by default.
3. Confirm provider environment:
   - `TRADINGAGENTS_LLM_PROVIDER`
   - quick/deep model settings if non-default models are needed
   - matching provider API key, unless provider is `ollama`
4. Create a `task.json`.
5. Run `python -m extensions.run.cli run ...`.
6. Read `result.json`.
7. Report status, final decision, output path, and a short summary.

## Setup Handoff

When setup is not ready, do not fail with a generic error. Use this decision table:

```text
No repo checkout:
  Follow tradingagents-setup. It uses the managed checkout at ~/.tradingagents/source/TradingAgents.

Missing Python dependencies or imports:
  Follow tradingagents-setup to install repo dependencies.

Missing provider selection:
  Ask which provider to use, or use the provider explicitly mentioned by the user.

Missing provider API key:
  Stop before analysis. Report the required env var and .env path.

Setup ready:
  Confirm external API/token usage, then run analysis.
```

If the user asked only to inspect prior outputs, do not run setup or analysis unless needed to locate files.

## Agent Report Format

For a completed run, summarize for the user:

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

For a blocked run due to credentials:

```text
Run status: blocked
Reason: missing provider credentials
Provider: <provider>
Required key: <env var>
Key value: not displayed
Next step: add <env var>=... to .env, then ask me to run again.
```

## Non-Interactive Task Runner

Automation path for Codex, Claude, opencode, CI, or batch jobs:

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
  "checkpoint_enabled": true
}
```

```bash
python -m extensions.run.cli run --task runs/nvda-2024-05-10/task.json --result-file runs/nvda-2024-05-10/result.json
```

The result JSON contains `status`, `decision`, `input_summary`, `analysis_summary`, `artifacts`, and structured error details.

## Interactive CLI

Interactive path for humans:

```bash
tradingagents analyze
tradingagents analyze --checkpoint
tradingagents analyze --clear-checkpoints
```

It prompts for ticker, date, output language, analysts, depth, provider, and models, then offers to save/display the full report.

## Python API

```python
import json

from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.graph.trading_graph import TradingAgentsGraph

config = DEFAULT_CONFIG.copy()
config["results_dir"] = "runs/nvda-2024-05-10"
config["max_debate_rounds"] = 1
config["max_risk_discuss_rounds"] = 1
config["output_language"] = "English"
config["checkpoint_enabled"] = True

graph = TradingAgentsGraph(
    selected_analysts=["market", "news", "fundamentals"],
    config=config,
)
final_state, decision = graph.propagate("NVDA", "2024-05-10", asset_type="stock")
print(json.dumps(final_state, indent=2, ensure_ascii=False))
print(decision)
```

## Environment

```bash
export TRADINGAGENTS_LLM_PROVIDER=openai
export TRADINGAGENTS_DEEP_THINK_LLM=gpt-5.5
export TRADINGAGENTS_QUICK_THINK_LLM=gpt-5.4-mini
export TRADINGAGENTS_OUTPUT_LANGUAGE=Chinese
export TRADINGAGENTS_MAX_DEBATE_ROUNDS=1
export TRADINGAGENTS_MAX_RISK_ROUNDS=1
export TRADINGAGENTS_RESULTS_DIR="$PWD/runs"
```

Also provide the selected provider key, such as `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or `GOOGLE_API_KEY`.

## Reading Outputs

- Interactive/API logs: `${results_dir}/${symbol}/TradingAgentsStrategy_logs/full_states_log_${analysis_date}.json`.
- Interactive saved reports: chosen save directory with `complete_report.md` and section files.
- Task runner output: `result.json`, with `analysis_summary` and `decision`.

Report the run status, final `decision`, output path, and short summary.

## Failure Handling

- Validation errors: bad JSON, invalid date, missing symbol, unsupported analyst, or unwritable `output_dir`.
- Configuration/model errors: missing API key, provider mismatch, bad model name, or invalid backend URL.
- Data unavailable errors: transient vendor issue or unsupported ticker; retry later or change data config.
- If a run is expensive, reduce `analysts` first, then reduce `research_depth`.
