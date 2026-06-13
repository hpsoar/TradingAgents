---
name: tradingagents-llm
description: Configure and diagnose TradingAgents LLM provider settings, model choices, API keys, reasoning controls, and custom endpoints without modifying source code. Use when setting environment variables, choosing quick/deep thinker models, or troubleshooting provider credentials and backend URLs across OpenAI, Anthropic, Google, Ollama, OpenRouter, Azure, xAI, DeepSeek, Qwen, GLM, and MiniMax.
---

# TradingAgents LLM Configuration

Use this skill only for runtime provider/model configuration, credential diagnosis, and endpoint debugging. For repo installation use `tradingagents-setup`; for running an analysis use `tradingagents-run`.

## Scope

Primary use cases:

- Set repeatable LLM provider/model environment variables.
- Debug provider keys, backend URLs, Ollama, OpenRouter, or Azure deployment settings.

Do not use this skill as the general setup flow or as the runbook for executing ticker analysis.
Do not use this skill to add providers, modify source code, maintain model catalogs, change validators, or update provider capabilities.

## User Intents

Use this skill when the user says things like:

- "Switch TradingAgents to DeepSeek."
- "Use qwen-cn with Chinese endpoint."
- "Configure Ollama on a remote server."
- "Why is my provider key not being picked up?"

For ordinary configuration requests, prefer updating `.env` through `tradingagents-setup` or direct non-secret edits. Do not ask the user to paste API key values into chat.

## Agent Report Format

For provider/model configuration, summarize:

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

## Quick Start

Use environment variables for repeatable, non-interactive runs:

```sh
export TRADINGAGENTS_LLM_PROVIDER=openai
export TRADINGAGENTS_QUICK_THINK_LLM=gpt-5.4-mini
export TRADINGAGENTS_DEEP_THINK_LLM=gpt-5.5
export OPENAI_API_KEY=...
```

Optional overrides:

```sh
export TRADINGAGENTS_LLM_BACKEND_URL=https://gateway.example.com/v1
export TRADINGAGENTS_TEMPERATURE=0
export OLLAMA_BASE_URL=http://localhost:11434/v1
```

The main config lives in `tradingagents/default_config.py`. Environment overrides are applied through `_ENV_OVERRIDES`; if a key is not listed there, setting an env var will not affect runtime behavior.

## Configuration Surface

Use these config keys when constructing `DEFAULT_CONFIG` overrides or debugging CLI selections:

- `llm_provider`: lower-case provider key, including `openai`, `anthropic`, `google`, `azure`, `xai`, `deepseek`, `qwen`, `qwen-cn`, `glm`, `glm-cn`, `minimax`, `minimax-cn`, `openrouter`, or `ollama`.
- `quick_think_llm`: fast model used by shallow/quick-thinking agents.
- `deep_think_llm`: stronger model used by deep-thinking agents.
- `backend_url`: custom endpoint. Leave as `None` to use provider defaults.
- `google_thinking_level`: Gemini thinking mode, usually `high` or `minimal`.
- `openai_reasoning_effort`: OpenAI reasoning effort, usually `low`, `medium`, or `high`.
- `anthropic_effort`: Claude extended-thinking effort, usually `low`, `medium`, or `high`.
- `temperature`: optional sampling temperature forwarded to providers that honor it.

## API Keys

Provider key names are fixed by the application. Use these env vars: `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, `GOOGLE_API_KEY`, `AZURE_OPENAI_API_KEY`, `XAI_API_KEY`, `DEEPSEEK_API_KEY`, `DASHSCOPE_API_KEY`, `DASHSCOPE_CN_API_KEY`, `ZHIPU_API_KEY`, `ZHIPU_CN_API_KEY`, `MINIMAX_API_KEY`, `MINIMAX_CN_API_KEY`, and `OPENROUTER_API_KEY`. Ollama requires no API key.

Do not hardcode secrets in config or skills. Use env vars or `.env`. Regional providers use separate accounts; international and China keys are not interchangeable.

## Choosing Models

Use the existing TradingAgents model choices and validation. Do not modify model catalogs from this skill.

- Use quick models for analyst loops where latency and cost matter.
- Use deep models for research managers, trading plans, and final decisions where reasoning quality matters more.
- For OpenRouter, Azure, and Ollama, custom model IDs or deployment names are expected.

## Custom Endpoints

Set `TRADINGAGENTS_LLM_BACKEND_URL` when routing through a proxy, gateway, self-hosted OpenAI-compatible server, or custom Azure/OpenRouter-style endpoint. For Ollama, prefer `OLLAMA_BASE_URL`; the default is `http://localhost:11434/v1`.

When debugging endpoint issues, inspect the current configured provider, backend URL, and environment overrides. Do not modify source files to change provider defaults.

## Verification

After changing `.env` or shell environment configuration, run the smallest relevant checks:

```sh
python -m cli.main --help
python -c "from tradingagents.default_config import DEFAULT_CONFIG; print(DEFAULT_CONFIG['llm_provider'])"
```
