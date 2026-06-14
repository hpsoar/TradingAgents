# Model Selection

Use existing TradingAgents model choices. Do not modify model catalogs.

## Config Keys

| Key | Purpose |
|---|---|
| `llm_provider` | Lower-case provider key |
| `quick_think_llm` | Fast model for quick agents |
| `deep_think_llm` | Stronger model for research manager, trader, portfolio manager |
| `backend_url` | Custom endpoint |
| `temperature` | Sampling temperature (lower = less variation) |
| `google_thinking_level` | Gemini: `high`, `minimal` |
| `openai_reasoning_effort` | OpenAI: `low`, `medium`, `high` |
| `anthropic_effort` | Claude: `low`, `medium`, `high` |

For OpenRouter, Azure, and Ollama, custom model IDs or deployment names are expected.

## Cost vs Quality

- `gpt-5.5` / `claude-4.6` / `gemini-3.1` for deep reasoning
- `gpt-5.4-mini` / `claude-4.5-sonnet` for quick tasks
- Lower `temperature` and non-reasoning models for more consistent output
