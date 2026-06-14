# Task Runner

## Task JSON schema

| Field | Type | Required | Default |
|---|---|---|---|
| `schema_version` | string | yes | `"1.0"` |
| `task_id` | string | yes | — |
| `symbol` | string | yes | — |
| `analysis_date` | string (YYYY-MM-DD) | yes | — |
| `output_dir` | string | yes | — |
| `asset_type` | string | no | `"stock"` |
| `analysts` | string[] | no | all four |
| `research_depth` | int | no | 1 |
| `output_language` | string | no | `"English"` |
| `llm_provider` | string | no | from .env or DEFAULT_CONFIG |
| `deep_think_llm` | string | no | from .env or DEFAULT_CONFIG |
| `quick_think_llm` | string | no | from .env or DEFAULT_CONFIG |
| `backend_url` | string | no | from .env or DEFAULT_CONFIG |
| `checkpoint_enabled` | bool | no | false |

## Example

```bash
mkdir -p runs/nvda-2024-05-10
```

task.json:
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
  "checkpoint_enabled": false
}
```

## Run command

```bash
python -m extensions.run.cli run \
  --task runs/nvda-2024-05-10/task.json \
  --result-file runs/nvda-2024-05-10/result.json
```

## Result JSON fields

| Field | Type | Description |
|---|---|---|
| `status` | string | success / validation_error / configuration_error / data_unavailable / model_error / internal_error |
| `decision` | string | strong_buy / buy / hold / sell / strong_sell |
| `input_summary` | object | Echo of task inputs |
| `analysis_summary` | object | Report texts per agent |
| `artifacts` | object | File paths produced |
| `error` | object | Structured error (code, message, retryable, details) |
| `started_at` | string | ISO 8601 |
| `finished_at` | string | ISO 8601 |
