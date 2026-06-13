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

## Execution Process

### 1. Check baseline files

- If `~/.tradingagents/source/TradingAgents/.env` is missing, use `tradingagents-setup` first.
- Read `.env` and the current process environment.

### 2. Read current values

- Read `TRADINGAGENTS_LLM_PROVIDER`, `TRADINGAGENTS_QUICK_THINK_LLM`, `TRADINGAGENTS_DEEP_THINK_LLM`, `TRADINGAGENTS_LLM_BACKEND_URL`, `TRADINGAGENTS_TEMPERATURE`, `OLLAMA_BASE_URL`, and provider credential env vars.
- Report credential status only as `present`, `missing`, or `not required`.

### 3. Validate requested values

- Validate provider keys with `references/provider-env.md`.
- Choose quick/deep models with `references/model-selection.md`.
- Configure endpoint values with `references/endpoints.md`.
- Stop if the provider is unsupported.

### 4. Edit `.env`

- Write only allowed `TRADINGAGENTS_*` settings, `OLLAMA_BASE_URL`, and empty credential placeholders.
- Preserve unrelated `.env` entries.
- Never write real API keys from chat.

### 5. Verify `.env`

- Re-read `.env` after editing.
- Confirm changed values match the request.
- Map provider to required credential env var; for `ollama`, use `not required`.
- If the required credential is missing, report the env var and stop before any provider call.

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
