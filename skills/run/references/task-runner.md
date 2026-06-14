# Task Runner

The non-interactive task runner is the recommended path for repeatable and batch analysis. Run from the project root.

## Task JSON Format

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
  "deep_think_llm": "gpt-5.5",
  "quick_think_llm": "gpt-5.4-mini",
  "backend_url": null,
  "checkpoint_enabled": false
}
```

## Run Command

```bash
python -m extensions.run.cli run \
  --task runs/nvda-2024-05-10/task.json \
  --result-file runs/nvda-2024-05-10/result.json
```

## Result JSON

```json
{
  "schema_version": "1.0",
  "task_id": "nvda-2024-05-10",
  "status": "success",
  "decision": "buy",
  "input_summary": { ... },
  "analysis_summary": {
    "market_report": "...",
    "sentiment_report": "...",
    "news_report": "...",
    "fundamentals_report": "...",
    "investment_plan": "...",
    "final_trade_decision": "..."
  },
  "artifacts": {
    "result.json": "/path/to/runs/nvda-2024-05-10/result.json"
  },
  "started_at": "2026-06-14T00:00:00",
  "finished_at": "2026-06-14T00:10:00"
}
```
