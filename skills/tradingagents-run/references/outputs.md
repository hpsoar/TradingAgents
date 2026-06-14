# Outputs

## Report format

```text
Run status: success | <error_code>
Symbol: NVDA
Analysis date: 2024-05-10
Decision: strong_buy | buy | hold | sell | strong_sell
Result file: runs/nvda-2024-05-10/result.json
Report files: runs/nvda-2024-05-10/result.json (artifacts)
Summary: <2-3 sentences>
Next step:
```

## Failure categories

| status | Meaning |
|---|---|
| `validation_error` | Bad JSON, missing fields, invalid date, bad analyst name, unwritable output_dir |
| `configuration_error` | Missing API key, unknown provider, bad model name, invalid backend URL |
| `data_unavailable` | Transient vendor issue, unsupported ticker |
| `model_error` | LLM call failed, rate limited, token limit exceeded |
| `internal_error` | Bug in TradingAgents code |

## Cost hints

- Fewer analysts = fewer LLM calls.
- Lower `research_depth` = fewer debate rounds.
- Use `quick_think_llm` instead of `deep_think_llm` for cheaper calls.
