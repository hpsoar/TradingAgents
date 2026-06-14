---
name: tradingagents-config
description: "Change LLM provider, deep/quick model, backend URL, output language, or sampling temperature for TradingAgents by editing .env. Use when: the user says 'switch to <provider>', 'use <model>', 'change language', 'configure endpoint', 'change settings', or another skill reports a configuration error. Do NOT use for initial setup — route first-time installation to tradingagents-setup."
allowed-tools: Bash(cat *), Bash(grep *), Bash(python *), Bash(test *)
---

# TradingAgents Config

Change runtime configuration by editing `.env`.

## Decision Tree

### Step 1 — Check that .env exists

```bash
test -f .env && echo "EXISTS" || echo "MISSING"
```

If `.env` is missing, route to `tradingagents-setup` and stop.

### Step 2 — Read current values

```bash
cat .env
```

Extract these values (they may be commented out):

| Key | Example |
|---|---|
| `TRADINGAGENTS_LLM_PROVIDER` | `openai` |
| `TRADINGAGENTS_DEEP_THINK_LLM` | `gpt-5.5` |
| `TRADINGAGENTS_QUICK_THINK_LLM` | `gpt-5.4-mini` |
| `TRADINGAGENTS_LLM_BACKEND_URL` | (empty or URL) |
| `TRADINGAGENTS_OUTPUT_LANGUAGE` | `English` |
| `TRADINGAGENTS_TEMPERATURE` | (empty or number) |
| `OLLAMA_BASE_URL` | (empty or URL) |

For credential env vars, report only `present` / `missing` — never display the value.

### Step 3 — Validate the requested changes

Supported providers (exact spelling):

```
openai, anthropic, google, azure, xai, deepseek,
qwen, qwen-cn, glm, glm-cn, minimax, minimax-cn,
openrouter, ollama
```

Stop and report `invalid provider` if the user asks for a provider not in this list.

For model names: accept any string. Do not validate against a catalog — the TradingAgents CLI handles model selection.

For `backend_url`: accept any `http://` or `https://` URL. Reject invalid URLs.

For `output_language`: accept `English` or `Chinese`. Reject anything else.

For `temperature`: accept a float string like `0.0`, `0.5`, `1.0`. Reject non-numeric values.

### Step 4 — Apply changes

Use the setup script to apply changes:

```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py \
  --provider <new_provider> \
  --deep-model <new_model> \
  --quick-model <new_model>
```

For targeted changes, pass only the flags the user asked for:

| Change | Flag |
|---|---|
| Change provider | `--provider <name>` |
| Change deep model | `--deep-model <name>` |
| Change quick model | `--quick-model <name>` |
| Change backend URL | `--backend-url <url>` |
| Change language | `--output-language <lang>` |

For Ollama endpoint changes, use:

```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py \
  --provider ollama \
  --backend-url http://ollama-host:11434/v1
```

### Step 5 — Verify changes

Read `.env` again and confirm the changed values match:

```bash
grep -E "^(TRADINGAGENTS_|OLLAMA_)" .env
```

If values do not match, report the discrepancy and stop.

### Step 6 — Check credentials

Map provider to required credential:

| Provider | Env var |
|---|---|
| openai | `OPENAI_API_KEY` |
| anthropic | `ANTHROPIC_API_KEY` |
| google | `GOOGLE_API_KEY` |
| azure | `AZURE_OPENAI_API_KEY` |
| xai | `XAI_API_KEY` |
| deepseek | `DEEPSEEK_API_KEY` |
| qwen | `DASHSCOPE_API_KEY` |
| qwen-cn | `DASHSCOPE_CN_API_KEY` |
| glm | `ZHIPU_API_KEY` |
| glm-cn | `ZHIPU_CN_API_KEY` |
| minimax | `MINIMAX_API_KEY` |
| minimax-cn | `MINIMAX_CN_API_KEY` |
| openrouter | `OPENROUTER_API_KEY` |
| ollama | (none required) |

Check if the env var is set in `.env` or the process environment:

```bash
grep "^<ENV_VAR>=" .env
```

If missing, report `Key status: missing` and tell the user to set it. Do NOT write the key value.

### Step 7 — Report

```text
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
Next step: Use tradingagents-run to run analysis.
```

## Allowed Writes

- `.env` entries for known `TRADINGAGENTS_*` settings and `OLLAMA_BASE_URL`.
- Empty credential placeholders (e.g., `OPENAI_API_KEY=`).

Never write real API key values received from the user in chat. Never modify source code, model catalogs, provider clients, or test files.

## Stop Conditions

- `.env` does not exist — route to setup first.
- Provider is not in the supported list.
- User provides a real API key in chat — tell them to set it in their environment or .env locally.
- User asks to add a new provider that isn't supported.
- Requested output language is not English or Chinese.

## References

- `references/provider-env.md` — full env var reference
- `references/model-selection.md` — model guidance
- `references/endpoints.md` — endpoint config
