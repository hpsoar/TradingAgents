---
name: setup
description: Install dependencies, configure .env, and verify TradingAgents is ready to run. Use when setting up TradingAgents for the first time or diagnosing environment issues.
---

# Setup

Prepare a TradingAgents checkout for use.

## Use When

- First-time setup after cloning the repo.
- Diagnose missing dependencies or broken imports.
- Install China market extras.
- Create an isolated virtual environment.
- Verify the project is ready before running analysis.

## Execution Process

### 1. Check prerequisites

Ensure the current directory is the TradingAgents project root (has `pyproject.toml` and `tradingagents/`).

### 2. Run setup script

```bash
python skills/setup/scripts/setup_tradingagents.py [options]
```

Common options:

| Flag | Purpose |
|---|---|
| `--provider <name>` | Set default LLM provider |
| `--deep-model <name>` | Model for deep-thinking agents |
| `--quick-model <name>` | Model for quick-thinking agents |
| `--backend-url <url>` | Custom API endpoint or Ollama URL |
| `--output-language <lang>` | Report language (English/Chinese) |
| `--venv <path>` | Create and use virtual env |
| `--china-extra` | Install China market dependencies |
| `--check-only` | Diagnose without writing |

### 3. Interpret results

| stdout/stderr pattern | Meaning |
|---|---|
| `Setup check passed.` | Everything ready |
| `WARNING: Missing OPENAI_API_KEY for provider 'openai'` | Ready but needs API key |
| `ERROR: ...` | Blocked, fix the error |

### 4. Route follow-up

- For provider or model changes after setup, use `config`.
- For running analysis, use `run`.

## Allowed Writes

- `.env` file: known `TRADINGAGENTS_*` settings, `OLLAMA_BASE_URL`, empty credential placeholders.
- `~/.tradingagents/` data directories (cache, logs, memory).
- Virtual environment at the requested path.
- Editable pip install into the current Python environment.

Never write real API key values from chat. Never clone the repo — it must already be checked out.

## Stop Conditions

- Python < 3.10.
- pip install failure.
- Project root cannot be detected.
- Required credential is missing and the user refuses to set it.

## Report Format

```
Setup status: ready | ready except credentials | blocked
Project root: /path/to/TradingAgents
Python: 3.12
Install: editable install (.)
Import tradingagents: ok
Provider: openai
Required key: OPENAI_API_KEY
Key status: present | missing | not required
Next step:
```

## References

- Setup script commands: `references/setup-commands.md`
- Provider keys and env vars: `references/provider-env.md`
- Verification checks: `references/verification.md`
