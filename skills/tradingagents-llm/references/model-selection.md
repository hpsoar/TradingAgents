# Model Selection

Use existing TradingAgents model choices and validation. Do not modify model catalogs from this skill.

Configuration keys:

- `llm_provider`: lower-case provider key.
- `quick_think_llm`: fast model used by shallow/quick-thinking agents.
- `deep_think_llm`: stronger model used by research managers, trading plans, and final decisions.
- `backend_url`: custom endpoint; leave empty to use provider defaults.
- `google_thinking_level`: Gemini thinking mode, usually `high` or `minimal`.
- `openai_reasoning_effort`: OpenAI reasoning effort, usually `low`, `medium`, or `high`.
- `anthropic_effort`: Claude extended-thinking effort, usually `low`, `medium`, or `high`.
- `temperature`: optional sampling temperature forwarded to providers that honor it.

For OpenRouter, Azure, and Ollama, custom model IDs or deployment names may be expected.
