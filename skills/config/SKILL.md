---
name: config
description: Change LLM provider, models, endpoint, or output language for TradingAgents. Use when the user wants to switch models, reconfigure the backend, or update .env settings after initial setup.
---

# Config

Change runtime configuration without rerunning setup.

## Use When

- Switch to a different LLM provider.
- Change deep-think or quick-think model.
- Configure a custom backend URL, proxy, or Ollama endpoint.
- Update output language or sampling temperature.
- Diagnose credential or connectivity issues.

## Execution Process

### 1. Read current config

Read `.env` from the project root. Report current values for:

- `TRADINGAGENTS_LLM_PROVIDER`
- `TRADINGAGENTS_DEEP_THINK_LLM`
- `TRADINGAGENTS_QUICK_THINK_LLM`
- `TRADINGAGENTS_LLM_BACKEND_URL`
- `TRADINGAGENTS_OUTPUT_LANGUAGE`
- `TRADINGAGENTS_TEMPERATURE`
- `OLLAMA_BASE_URL`

Report credential status as `present`, `missing`, or `not required` — never display the actual key value.

### 2. Validate requested changes

- Validate provider name against the supported list: `openai`, `anthropic`, `google`, `azure`, `xai`, `deepseek`, `qwen`, `qwen-cn`, `glm`, `glm-cn`, `minimax`, `minimax-cn`, `openrouter`, `ollama`.
- Validate model names against the TradingAgents model catalog (do not modify source files).
- For custom endpoints, accept any valid URL.
- For Ollama, use `OLLAMA_BASE_URL` instead of `TRADINGAGENTS_LLM_BACKEND_URL`.

### 3. Apply changes

Edit `.env` using the setup script's upsert logic:

```bash
python skills/setup/scripts/setup_tradingagents.py \
  --provider openai \
  --deep-model gpt-5.5 \
  --quick-model gpt-5.4-mini
```

Or for targeted changes, directly edit `.env`:

| Key | Example |
|---|---|
| `TRADINGAGENTS_LLM_PROVIDER` | `openai` |
| `TRADINGAGENTS_DEEP_THINK_LLM` | `gpt-5.5` |
| `TRADINGAGENTS_QUICK_THINK_LLM` | `gpt-5.4-mini` |
| `TRADINGAGENTS_LLM_BACKEND_URL` | `http://proxy:8080/v1` |
| `TRADINGAGENTS_OUTPUT_LANGUAGE` | `Chinese` |
| `TRADINGAGENTS_TEMPERATURE` | `0.3` |
| `OLLAMA_BASE_URL` | `http://ollama-host:11434/v1` |

### 4. Verify

Re-read `.env` and confirm the changed values match the request.

If the provider needs a credential that is still missing, report the env var.

### 5. Route follow-up

- For running analysis after config, use `run`.

## Allowed Writes

- `.env` entries for known `TRADINGAGENTS_*` settings.
- `OLLAMA_BASE_URL` for non-default Ollama endpoints.
- Empty credential placeholders when useful (e.g. `OPENAI_API_KEY=`).

Do not write real API keys from chat. Do not modify source code, model catalogs, provider clients, or test files.

## Stop Conditions

- Provider is not in the supported list.
- `.env` does not exist (route to `setup` first).
- User provides a real API key value in chat — ask them to set it locally.
- User asks to implement a new provider.

## Report Format

```
Config status: updated | blocked | unchanged
Provider: openai
Deep model: gpt-5.5
Quick model: gpt-5.4-mini
Backend URL: (not set)
Output language: English
Temperature: (not set)
Required key: OPENAI_API_KEY
Key status: present | missing | not required
Key value: not displayed
Files changed: .env
Next step:
```

## References

- Provider key mapping: `references/provider-env.md`
- Model selection guidance: `references/model-selection.md`
- Endpoint configuration: `references/endpoints.md`
