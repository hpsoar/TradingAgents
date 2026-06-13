# Run Modes

Prefer the non-interactive task runner for agent automation.

Interactive path for humans:

```bash
tradingagents analyze
tradingagents analyze --checkpoint
tradingagents analyze --clear-checkpoints
```

It prompts for ticker, date, output language, analysts, depth, provider, and models, then offers to save or display the full report.

Python API path:

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
