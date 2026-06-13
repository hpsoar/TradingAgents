---
name: tradingagents-setup
description: Set up TradingAgents for local or package-based use by installing dependencies, preparing .env provider settings, creating cache/log/memory directories, and checking runtime readiness. Use when a user asks to install, configure, bootstrap, verify, or troubleshoot TradingAgents setup across Codex, Claude, opencode, or another coding agent.
---

# TradingAgents Setup

Use this skill to prepare a TradingAgents checkout or installed package for a first run without hard-coding user secrets.

## Quick Start

From a TradingAgents repo checkout:

```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py --provider openai --deep-model gpt-5.5 --quick-model gpt-5.4-mini
```

From no checkout:

```bash
python /path/to/skills/tradingagents-setup/scripts/setup_tradingagents.py --project-dir ./TradingAgents --repo-url git@github.com:hpsoar/TradingAgents.git --ref v1.0 --provider openai
```

For package-only installation:

```bash
mkdir -p ./tradingagents-run
python /path/to/skills/tradingagents-setup/scripts/setup_tradingagents.py --project-dir ./tradingagents-run --install package --provider openai
```

The helper is the primary setup entrypoint. Full project setup means a repo checkout plus its local package metadata, CLI package, optional China market package, `.env`, data directories, provider credentials, and readiness checks. Package-only setup is limited: it installs the published `tradingagents` package for library/CLI use, but it is not a substitute for setting up this repository.

## Setup Workflow

1. Confirm Python is 3.10 or newer.
2. Run the setup helper:
   - In a repo checkout, it reuses that checkout and defaults to `pip install -e .`.
   - Outside a checkout, pass `--project-dir <dir>`; full setup clones the TradingAgents repo there before installing.
   - Use `--repo-url <url>` and `--ref <branch-or-tag-or-sha>` when the default repo/ref is not the desired source.
   - Outside a checkout, pass both `--project-dir <dir>` and `--install package` only for package-only mode; this is not full project setup.
   - Use `--install local`, `--install package`, or `--install skip` to override the default.
   - Use `--china-extra` when China market dependencies are needed.
   - Use `--venv .venv` when the user wants an isolated virtual environment.
3. Create `.env`:
   - Copy `.env.example` to `.env` when `.env` does not exist.
   - If there is no repo checkout, require `--project-dir <dir>` so `.env` is not written to an accidental current directory.
   - Do not invent, log, or commit API keys.
   - Set one provider key for the selected LLM provider.
4. Configure provider selection with `TRADINGAGENTS_*` variables when unattended runs should skip CLI prompts.
5. Create default data directories:
   - `~/.tradingagents/cache`
   - `~/.tradingagents/logs`
   - `~/.tradingagents/memory`
6. Run a readiness check and report exact missing items.

## Dependency Coverage

For this repo, do not treat `pip install tradingagents` as enough for full setup. Full setup must ensure a TradingAgents repo checkout exists first. If the helper is not already running inside one, it should clone `--repo-url` into `--project-dir`, checkout `--ref`, then run `pip install -e .` so the repo's declared project dependencies from `pyproject.toml` are installed and these local packages are exposed:

```text
tradingagents
cli
china_market
```

Base dependencies include LangChain/LangGraph provider packages, pandas, yfinance, stockstats, redis client, rich, typer, questionary, requests, tqdm, and related runtime libraries declared in `pyproject.toml`.

Use `--china-extra` when the user needs China market providers; it installs the optional `china` dependency group (`akshare`, `baostock`, `tushare`). External credentials and services are still separate readiness items, not Python packages:

```text
LLM provider API key or Ollama endpoint
Optional ALPHA_VANTAGE_API_KEY
Optional running Ollama service for provider=ollama
Optional Docker/Compose path when the user wants container setup
```

## Provider Environment

Set at least one provider key that matches the intended LLM provider:

```bash
OPENAI_API_KEY=
GOOGLE_API_KEY=
ANTHROPIC_API_KEY=
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

Optional data keys:

```bash
ALPHA_VANTAGE_API_KEY=
```

For Ollama, no API key is required. Use `OLLAMA_BASE_URL` only when the endpoint is not the local default `http://localhost:11434/v1`.

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

## Readiness Check

Prefer the bundled helper for both setup and checks:

```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py --check-only
```

Useful options:

```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py --provider google --deep-model gemini-3.1-pro --quick-model gemini-3.1-flash
python skills/tradingagents-setup/scripts/setup_tradingagents.py --provider ollama --backend-url http://localhost:11434/v1
python skills/tradingagents-setup/scripts/setup_tradingagents.py --cache-dir ./data/cache --results-dir ./data/logs --memory-log ./data/memory/trading_memory.md
python /path/to/skills/tradingagents-setup/scripts/setup_tradingagents.py --project-dir ./TradingAgents --repo-url git@github.com:hpsoar/TradingAgents.git --ref v1.0 --provider openai
python /path/to/skills/tradingagents-setup/scripts/setup_tradingagents.py --project-dir ./tradingagents-run --install package --provider openai
python skills/tradingagents-setup/scripts/setup_tradingagents.py --venv .venv --provider openai
python skills/tradingagents-setup/scripts/setup_tradingagents.py --china-extra --provider dashscope_cn
```

The helper is safe to rerun. It reuses existing repo checkouts, refuses non-empty non-repo target directories, preserves existing `.env` values, creates missing directories, installs dependencies unless `--install skip` or `--check-only` is used, checks required imports, and prints warnings for missing keys.

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
