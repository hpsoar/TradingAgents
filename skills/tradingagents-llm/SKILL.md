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

### 1. Read current LLM config

- Read `.env` in the fixed TradingAgents project directory, `~/.tradingagents/source/TradingAgents`, and the current process environment.
- Check these settings: `TRADINGAGENTS_LLM_PROVIDER`, `TRADINGAGENTS_QUICK_THINK_LLM`, `TRADINGAGENTS_DEEP_THINK_LLM`, `TRADINGAGENTS_LLM_BACKEND_URL`, `TRADINGAGENTS_TEMPERATURE`, and provider credential env vars.
- Report credential status only as `present`, `missing`, or `not required`.

### 2. Validate requested config

- Validate the provider against `references/provider-env.md`.
- Use `references/model-selection.md` when choosing quick/deep models.
- Use `references/endpoints.md` when configuring custom backend URLs, Azure/OpenRouter-style endpoints, proxies, or Ollama.
- If the provider is unsupported, stop; do not edit source code or invent provider support.

### 3. Apply config

- Edit only `.env`.
- Write only allowed `TRADINGAGENTS_*` settings, `OLLAMA_BASE_URL`, and empty credential placeholders.
- Preserve unrelated `.env` entries.
- Never write real API keys from chat.

### 4. Verify config

- Re-read `.env` after editing.
- Verify the selected provider value is present.
- Verify quick/deep model values match the requested values or the chosen defaults.
- Verify backend URL and temperature values match the request when provided.
- Map the provider to its required credential env var; for `ollama`, mark key status as `not required`.
- If the required credential is missing, stop before any provider call and report the exact env var to set.

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
