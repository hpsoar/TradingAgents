---
name: tradingagents-setup
description: Set up or diagnose a local TradingAgents repository checkout by installing repo dependencies, preparing .env provider settings, creating cache/log/memory directories, and checking runtime readiness. Use when a user asks to install, configure, bootstrap, verify, or troubleshoot a TradingAgents repo for Codex, Claude, opencode, or another coding agent. Do not use this as a package-only install guide.
---

# TradingAgents Setup

Use this skill to prepare a local TradingAgents repo checkout for first run without hard-coding user secrets.

## User Intents

Use this skill when the user says things like:

- "Set up TradingAgents."
- "Configure TradingAgents with OpenAI/DeepSeek/Qwen/Ollama."
- "Check whether TradingAgents can run."
- "Fix my TradingAgents environment."

The user should not need to know or type the helper command. The agent should run the helper, inspect the result, and report a concise status.

## Scope

Primary use case: a source checkout of this repository.

Do not treat `pip install tradingagents` as a complete setup for these skills. Package-only installation is only useful when another project wants to import the published package or run the published CLI. It does not provide this repo's `extensions/run` automation entrypoint, local tests, or source-edit workflow.

## Default Flow

1. Detect the current state before making changes:
   - Confirm Python is 3.10 or newer.
   - Confirm the working directory is a TradingAgents repo checkout (`pyproject.toml` plus `tradingagents/`).
   - Check whether `.env` exists.
   - Check whether a virtual environment is already in use or requested.
2. Decide the setup mode:
   - Always use the managed checkout at `~/.tradingagents/source/TradingAgents`.
   - If that path is already a TradingAgents repo, reuse it.
   - If that path does not exist or is empty, clone the repo there.
   - If that path exists, is non-empty, and is not a TradingAgents repo, stop and report the conflict.
   - Check-only request: diagnose only; do not install dependencies or write files.
3. Configure the repo:
   - Copy `.env.example` to `.env` when `.env` does not exist.
   - Do not invent, log, or commit API keys.
   - Write only known `TRADINGAGENTS_*` overrides requested by the user.
   - Use canonical provider keys: `openai`, `anthropic`, `google`, `azure`, `xai`, `deepseek`, `qwen`, `qwen-cn`, `glm`, `glm-cn`, `minimax`, `minimax-cn`, `openrouter`, or `ollama`.
4. Install dependencies:
   - Default repo install: `python -m pip install -e .`
   - China market extras: `python -m pip install -e .[china]`
   - Optional venv: create/use the requested venv first.
5. Create default data paths when missing:
   - `~/.tradingagents/cache`
   - `~/.tradingagents/logs`
   - `~/.tradingagents/memory`
6. Verify readiness:
   - Import `tradingagents` and `cli`.
   - Check the selected provider has the required key, unless provider is `ollama`.
   - Verify the CLI starts.
   - Report exact missing items and next commands.

## Agent Report Format

Do not paste raw helper output as the final answer. Summarize it for the user:

```text
Setup status: ready | ready except credentials | blocked
Project dir: <path>
Python: <path/version>
Install: <installed/skipped/check-only/would install>
Provider: <provider or not configured>
Required key: <env var or none>
Key status: present | missing | not required
Key value: not displayed
Next step: <one concrete action>
```

If credentials are missing, tell the user which variable to add to `.env` or their shell environment. Do not ask the user to paste API keys into chat.

Example:

```text
Setup status: ready except credentials
Project dir: /path/to/TradingAgents
Provider: qwen-cn
Required key: DASHSCOPE_CN_API_KEY
Key status: missing
Key value: not displayed
Next step: add DASHSCOPE_CN_API_KEY=... to .env, then ask me to re-check.
```

## Helper Commands

These commands are implementation details for the agent.

From a TradingAgents repo checkout:


```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py --provider openai --deep-model gpt-5.5 --quick-model gpt-5.4-mini
```

With an isolated venv:

```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py --venv .venv --provider openai
```

For China market dependencies:

```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py --china-extra --provider qwen-cn
```

From outside a checkout, use the fixed managed checkout at `~/.tradingagents/source/TradingAgents`:

```bash
python /path/to/skills/tradingagents-setup/scripts/setup_tradingagents.py --provider openai
```

## Check Only

Use check-only for diagnosis. It must not be described as a completed setup because it skips writes and installs.

```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py --check-only
```

## Provider Environment

Set one provider key that matches the intended LLM provider:

```bash
OPENAI_API_KEY=
GOOGLE_API_KEY=
ANTHROPIC_API_KEY=
AZURE_OPENAI_API_KEY=
XAI_API_KEY=
DEEPSEEK_API_KEY=
DASHSCOPE_API_KEY=
DASHSCOPE_CN_API_KEY=
ZHIPU_API_KEY=
ZHIPU_CN_API_KEY=
MINIMAX_API_KEY=
MINIMAX_CN_API_KEY=
OPENROUTER_API_KEY=
```

Provider key mapping:

```text
openai      -> OPENAI_API_KEY
google      -> GOOGLE_API_KEY
anthropic   -> ANTHROPIC_API_KEY
azure       -> AZURE_OPENAI_API_KEY
xai         -> XAI_API_KEY
deepseek    -> DEEPSEEK_API_KEY
qwen        -> DASHSCOPE_API_KEY
qwen-cn     -> DASHSCOPE_CN_API_KEY
glm         -> ZHIPU_API_KEY
glm-cn      -> ZHIPU_CN_API_KEY
minimax     -> MINIMAX_API_KEY
minimax-cn  -> MINIMAX_CN_API_KEY
openrouter  -> OPENROUTER_API_KEY
ollama      -> no API key
```

Optional data key:

```bash
ALPHA_VANTAGE_API_KEY=
```

For Ollama, use `OLLAMA_BASE_URL` only when the endpoint is not the local default `http://localhost:11434/v1`.

## Unattended Configuration

Use these `.env` overrides to avoid interactive provider/model prompts:

```bash
TRADINGAGENTS_LLM_PROVIDER=openai
TRADINGAGENTS_DEEP_THINK_LLM=gpt-5.5
TRADINGAGENTS_QUICK_THINK_LLM=gpt-5.4-mini
TRADINGAGENTS_LLM_BACKEND_URL=
TRADINGAGENTS_OUTPUT_LANGUAGE=English
TRADINGAGENTS_MAX_DEBATE_ROUNDS=1
TRADINGAGENTS_MAX_RISK_ROUNDS=1
TRADINGAGENTS_CHECKPOINT_ENABLED=false
TRADINGAGENTS_TEMPERATURE=0.0
```

Use `TRADINGAGENTS_CACHE_DIR`, `TRADINGAGENTS_RESULTS_DIR`, and `TRADINGAGENTS_MEMORY_LOG_PATH` only when the default `~/.tradingagents` layout is not appropriate.

## Verification

After setup, verify the CLI starts:

```bash
tradingagents --help
```

From a source checkout, this direct form also works:

```bash
python -m cli.main --help
```

Do not run a full trading analysis as a setup check unless the user explicitly approves external API calls and token usage.
