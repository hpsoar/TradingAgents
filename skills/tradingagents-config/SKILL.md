---
name: tradingagents-config
description: "Change LLM provider, deep/quick model, endpoint, output language, or temperature for TradingAgents. Use when: the user says 'switch to <provider>', 'use <model>', 'change language', 'configure endpoint', 'change settings'; or tradingagents-run reports a configuration_error. Do NOT use for initial setup — route first-time installation to tradingagents-setup."
allowed-tools: Bash(cat *), Bash(grep *), Bash(test *), Bash(echo *), Bash(sed *)
---

# TradingAgents Config

Change runtime configuration by editing `.env` in the setup project root.

## Prerequisites

`tradingagents-setup` must have completed successfully.

## Decision Tree

### Step 1 — Verify setup is complete

```bash
test -f ~/.tradingagents/.setup_done && echo "STAMP_OK" || echo "STAMP_MISSING"
PROJECT_DIR=$(cat ~/.tradingagents/.setup_done 2>/dev/null)
```

If `STAMP_MISSING` or `PROJECT_DIR` is empty, route to `tradingagents-setup` and stop.

Read the project root from the stamp. All subsequent commands run from `$PROJECT_DIR`.

```bash
test -f "$PROJECT_DIR/.env" && echo "ENV_EXISTS" || echo "ENV_MISSING"
```

If `.env` is missing, route to `tradingagents-setup` (it creates the .env from template).

### Step 2 — Read current values

```bash
cat "$PROJECT_DIR/.env"
```

Extract these (they may be commented out):

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

### Step 3 — Validate requested changes

Supported providers (exact spelling):

```
openai, anthropic, google, azure, xai, deepseek,
qwen, qwen-cn, glm, glm-cn, minimax, minimax-cn,
openrouter, ollama
```

Stop if user asks for a provider not in this list.

For model names: accept any string (TradingAgents CLI handles model selection).

For `backend_url`: accept any `http://` or `https://` URL.

For `output_language`: accept `English` or `Chinese` only.

For `temperature`: accept a float string like `0.0`, `0.5`, `1.0`.

### Step 4 — Apply changes

Use `sed` to update or uncomment specific keys in `.env`:

```bash
# Set or replace TRADINGAGENTS_LLM_PROVIDER
sed -i 's/^#\?TRADINGAGENTS_LLM_PROVIDER=.*/TRADINGAGENTS_LLM_PROVIDER=openai/' "$PROJECT_DIR/.env"
```

Pattern for each possible change:

| Key | sed pattern |
|---|---|
| `TRADINGAGENTS_LLM_PROVIDER` | `s/^#\?TRADINGAGENTS_LLM_PROVIDER=.*/TRADINGAGENTS_LLM_PROVIDER=<value>/` |
| `TRADINGAGENTS_DEEP_THINK_LLM` | `s/^#\?TRADINGAGENTS_DEEP_THINK_LLM=.*/TRADINGAGENTS_DEEP_THINK_LLM=<value>/` |
| `TRADINGAGENTS_QUICK_THINK_LLM` | `s/^#\?TRADINGAGENTS_QUICK_THINK_LLM=.*/TRADINGAGENTS_QUICK_THINK_LLM=<value>/` |
| `TRADINGAGENTS_LLM_BACKEND_URL` | `s/^#\?TRADINGAGENTS_LLM_BACKEND_URL=.*/TRADINGAGENTS_LLM_BACKEND_URL=<url>/` |
| `TRADINGAGENTS_OUTPUT_LANGUAGE` | `s/^#\?TRADINGAGENTS_OUTPUT_LANGUAGE=.*/TRADINGAGENTS_OUTPUT_LANGUAGE=<lang>/` |
| `TRADINGAGENTS_TEMPERATURE` | `s/^#\?TRADINGAGENTS_TEMPERATURE=.*/TRADINGAGENTS_TEMPERATURE=<value>/` |
| `OLLAMA_BASE_URL` | `s/^#\?OLLAMA_BASE_URL=.*/OLLAMA_BASE_URL=<url>/` |

If a key does not exist at all in the file (commented or not), append it.

### Step 5 — Verify

```bash
grep -E "^(TRADINGAGENTS_|OLLAMA_)" "$PROJECT_DIR/.env"
```

Confirm changed values match. If not, report discrepancy and stop.

### Step 6 — Check credentials

Map provider to credential:

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
| ollama | (none) |

```bash
grep "^<ENV_VAR>=" "$PROJECT_DIR/.env"
```

If missing, report `Key status: missing`. Do NOT write the key value.

### Step 7 — Report

```
Config status: updated | blocked | unchanged
Project dir: /home/user/.tradingagents/source/TradingAgents
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

- `.env` in the project root — only known `TRADINGAGENTS_*` settings and `OLLAMA_BASE_URL`.
- Empty credential placeholders (e.g., `OPENAI_API_KEY=`).

Never write real API key values. Never modify source code, model catalogs, or test files.

## Stop Conditions

- Setup stamp is missing — route to setup first.
- `.env` does not exist — route to setup first.
- Provider not in supported list.
- User provides a real API key in chat — tell them to set it locally.
- Requested output language is not English or Chinese.

## References

- `references/provider-env.md` — full env var reference
- `references/model-selection.md` — model guidance
- `references/endpoints.md` — endpoint config
