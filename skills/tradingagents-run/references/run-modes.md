# Run Modes

## Task runner (preferred for agent automation)

```bash
python -m extensions.run.cli run --task <task.json> --result-file <result.json>
```

## Interactive CLI

```bash
tradingagents analyze
tradingagents analyze --checkpoint
tradingagents analyze --clear-checkpoints
```

## Python API

```python
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.graph.trading_graph import TradingAgentsGraph

config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "openai"
config["output_language"] = "English"

ta = TradingAgentsGraph(selected_analysts=["market", "news"], config=config)
_, decision = ta.propagate("NVDA", "2024-05-10", asset_type="stock")
print(decision)
```
