---
name: tradingagents-llm
description: Configure or diagnose TradingAgents LLM settings. Use when the user asks to choose a provider or model, configure credential environment variables, configure endpoints, or troubleshoot LLM connectivity.
---

# TradingAgents LLM Configuration

Configure and diagnose runtime LLM settings only.

## Use When

- Switch TradingAgents to an existing provider.
- Choose quick/deep thinker models.
- Configure custom backend URLs, proxies, Azure/OpenRouter-style endpoints, or Ollama.
- Diagnose missing credentials or environment variables.
- Explain which local `.env` setting controls LLM behavior.

## Default Flow

1. Identify the requested provider, models, endpoint, and reasoning controls.
2. Validate the provider against the existing supported provider keys.
3. Determine the required credential env var, unless the provider is `ollama`.
4. Update only non-secret local configuration when requested.
5. For missing credentials, stop and report the required env var.
6. For endpoint issues, inspect current env settings and configured provider; do not change source defaults.
7. Run a lightweight verification check when configuration changes.
8. Report the effective provider/model/key status and next step.

## Allowed Writes

- `.env` entries for known `TRADINGAGENTS_*` configuration.
- Empty credential placeholders when useful, such as `OPENAI_API_KEY=`.

Do not write real secrets, source files, model catalogs, validators, provider clients, or tests from this skill.

## Allowed Configuration

- `TRADINGAGENTS_LLM_PROVIDER`
- `TRADINGAGENTS_QUICK_THINK_LLM`
- `TRADINGAGENTS_DEEP_THINK_LLM`
- `TRADINGAGENTS_LLM_BACKEND_URL`
- `TRADINGAGENTS_TEMPERATURE`
- Provider-specific credential env vars
- `OLLAMA_BASE_URL` for non-default Ollama endpoints
- Existing reasoning-control env vars supported by the application

## Stop Conditions

- The provider is not supported by the existing application.
- The required API key is missing.
- The user asks to add or implement provider support.
- The user provides real API key values in chat; ask them to set secrets locally instead.

## Report Format

```text
LLM config status: updated | blocked | unchanged
Provider:
Quick model:
Deep model:
Backend URL:
Required key:
Key status: present | missing | not required
Key value: not displayed
Files changed:
Next step:
```

## References

- Provider key mapping and common env vars: `references/provider-env.md`
- Endpoint configuration: `references/endpoints.md`
- Model selection guidance: `references/model-selection.md`
