# Task Runner

The non-interactive task runner is the recommended automation path for repeatable or batch analysis. Run it from the fixed TradingAgents project directory: `~/.tradingagents/source/TradingAgents`.

Example task:

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

Run it with:

```bash
cd ~/.tradingagents/source/TradingAgents
python -m extensions.run.cli run --task runs/nvda-2024-05-10/task.json --result-file runs/nvda-2024-05-10/result.json
```

The result JSON contains `status`, `decision`, `input_summary`, `analysis_summary`, `artifacts`, and structured error details.
