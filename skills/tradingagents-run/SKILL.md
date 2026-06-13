---
name: tradingagents-run
description: Run TradingAgents financial analysis through the interactive CLI, the non-interactive task runner, or the Python API, then locate and summarize saved reports. Use when the user asks to analyze a ticker, choose TradingAgents analysts, set research depth/debate rounds, set report language, save reports, inspect prior TradingAgents outputs, or automate TradingAgents runs from an agent.
---

# TradingAgents Run
## Inputs
- `symbol`: ticker with suffix when needed: `NVDA`, `0700.HK`, `600519.SS`, `BTC-USD`.
- `analysis_date`: `YYYY-MM-DD`; do not use a future date.
- `asset_type`: usually `stock`; use `crypto` for crypto symbols.
- `analysts`: subset of `market`, `social`, `news`, `fundamentals`; omit for all four.
- `research_depth`: integer debate depth; `1` is fastest, higher values cost more.
- `output_language`: report language, such as `English` or `Chinese`.
- Model/provider settings and API keys. Prefer environment variables for repeatable agent runs.
## CLI
Interactive path for humans:

```bash
tradingagents analyze
tradingagents analyze --checkpoint
tradingagents analyze --clear-checkpoints
```

It prompts for ticker, date, output language, analysts, depth, provider, and
models, then offers to save/display the full report.
## Non-interactive task runner
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

The result JSON contains `status`, `decision`, `input_summary`,
`analysis_summary`, `artifacts`, and structured error details.
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

Also provide the selected provider key, such as `OPENAI_API_KEY`,
`ANTHROPIC_API_KEY`, or `GOOGLE_API_KEY`.
## Reading Outputs
- Interactive/API logs: `${results_dir}/${symbol}/TradingAgentsStrategy_logs/full_states_log_${analysis_date}.json`.
- Interactive saved reports: chosen save directory with `complete_report.md` and section files.
- Task runner output: `result.json`, with `analysis_summary` and `decision`.

Report the run status, final `decision`, output path, and short summary.
## Failure Handling
- Validation errors: bad JSON, invalid date, missing symbol, or unwritable `output_dir`.
- Configuration/model errors: missing API key, provider mismatch, bad model name, or invalid backend URL.
- Data unavailable errors: transient vendor issue or unsupported ticker; retry later or change data config.
- If a run is expensive, reduce `analysts` first, then reduce `research_depth`.
