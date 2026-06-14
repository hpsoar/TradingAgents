# Outputs

## Result Fields

| Field | Description |
|---|---|
| `status` | `success`, `validation_error`, `configuration_error`, `data_unavailable`, `model_error`, `internal_error` |
| `decision` | `strong_buy`, `buy`, `hold`, `sell`, `strong_sell` |
| `input_summary` | Echo of task inputs |
| `analysis_summary` | Report texts from each agent |
| `artifacts` | File paths produced by the run |
| `error` | Structured error (code, message, retryable, details) |

## Failure Categories

- **Validation errors**: bad JSON, missing fields, invalid date, bad analyst name.
- **Configuration/model errors**: missing API key, unknown provider, bad model name.
- **Data unavailable**: vendor issue or unsupported ticker.

## Cost Control

- Reduce `analysts` list first, then reduce `research_depth`.
- Use `quick_think_llm` for cheaper analysis.
