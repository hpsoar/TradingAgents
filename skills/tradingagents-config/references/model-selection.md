# Model Selection

Do NOT modify model catalog source files. Use existing TradingAgents model choices.

## Config keys

| Key | Purpose |
|---|---|
| `TRADINGAGENTS_LLM_PROVIDER` | Lower-case provider key |
| `TRADINGAGENTS_QUICK_THINK_LLM` | Fast model for analysts (sentiment, news, technical, fundamentals) |
| `TRADINGAGENTS_DEEP_THINK_LLM` | Strong model for research manager, trader, portfolio manager |
| `TRADINGAGENTS_LLM_BACKEND_URL` | Custom API endpoint for OpenAI-compatible proxy |
| `TRADINGAGENTS_TEMPERATURE` | Sampling temperature; lower = less variation |
| `OLLAMA_BASE_URL` | Ollama endpoint (default: http://localhost:11434/v1) |

## Cost guidance

- Deep models (gpt-5.5, claude-4.6, gemini-3.1): best quality, most expensive
- Quick models (gpt-5.4-mini, claude-4.5-sonnet): good enough for analysts, cheaper
- Lower temperature + non-reasoning models = more consistent output
