---
name: tradingagents-setup
description: Set up or diagnose TradingAgents. Use when the user asks to install, configure, verify, or troubleshoot the local TradingAgents environment.
---

# TradingAgents Setup

Prepare the local TradingAgents environment without hard-coding, exposing, or inventing user secrets.

## Use When

- Set up TradingAgents for the first time.
- Configure non-secret provider/model defaults.
- Check whether the TradingAgents project directory can run.
- Diagnose missing dependencies, `.env`, data directories, or credentials.

## Execution Process

### 1. Identify what will be set up

- TradingAgents fixed project directory: `~/.tradingagents/source/TradingAgents`.
- Python runtime: must be Python 3.10 or newer.
- Optional virtual environment: use the user-requested venv, otherwise keep the current environment.
- Local config: `.env` in the fixed project directory.
- Local data dirs: `~/.tradingagents/cache`, `~/.tradingagents/logs`, and `~/.tradingagents/memory`.

### 2. Check current state first

Run these checks before changing anything:

```bash
cd ~/.tradingagents/source/TradingAgents
test -d tradingagents
test -d cli
test -f extensions/run/cli.py
python --version
test -f .env
test -d ~/.tradingagents/cache
test -d ~/.tradingagents/logs
test -d ~/.tradingagents/memory
```

- If only checking or diagnosing, stop after reporting which checks passed and failed.
- If `cd ~/.tradingagents/source/TradingAgents` fails, create or clone the project there.
- If `~/.tradingagents/source/TradingAgents` exists but does not contain `tradingagents/`, `cli/`, and `extensions/run/cli.py`, stop.

### 3. Do the setup work

- If Python is older than 3.10, stop before installing dependencies.
- If the user requested a venv, create or reuse that venv and run later commands inside it.
- Install project dependencies with the helper script or the repo's normal install command.
- If `.env` is missing, create it from `.env.example`; if `.env.example` is missing, create only the known `TRADINGAGENTS_*` entries needed for unattended runs.
- Write only requested non-secret settings such as provider, models, backend URL, output language, debate rounds, checkpoint flag, and temperature.
- Create missing data dirs under `~/.tradingagents`.

### 4. Verify what setup changed

Run the checks that match the setup work:

```bash
cd ~/.tradingagents/source/TradingAgents
python -c "import tradingagents; import cli"
python -m cli.main --help
python -m extensions.run.cli --help
test -f .env
test -d ~/.tradingagents/cache
test -d ~/.tradingagents/logs
test -d ~/.tradingagents/memory
```

- Dependency install is valid only if the import command succeeds.
- CLI setup is valid only if both `python -m cli.main --help` and `python -m extensions.run.cli --help` succeed.
- Config setup is valid only if `.env` exists and contains the selected `TRADINGAGENTS_LLM_PROVIDER`.
- Data-dir setup is valid only if all three `~/.tradingagents` directories exist.
- Credential readiness is valid only if the selected provider's required env var is present; for `ollama`, no API key is required.

### 5. Report readiness

- Report `ready` only when fixed project directory, Python, dependencies, CLI, config, data dirs, provider, and credential checks pass.
- Report `ready except credentials` only when all checks pass except the required credential env var.
- Report `blocked` with the exact failed check and next command or action.

## Allowed Writes

- `.env`, but only for known non-secret `TRADINGAGENTS_*` settings and empty credential placeholders.
- Requested virtual environment directories.
- Default data directories: `~/.tradingagents/cache`, `~/.tradingagents/logs`, `~/.tradingagents/memory`.
- Dependency installation into the selected environment.

Never write real API key values unless they already exist in the user's local environment or files. Never ask the user to paste keys into chat.

## Stop Conditions

- The fixed project directory exists, is non-empty, and is not a TradingAgents project directory.
- Python is older than 3.10.
- Required credentials are missing after setup; report the env var and mark readiness as incomplete.
- The requested provider key is unsupported by the existing application.
- Network or package installation is blocked and user approval is required.

## Report Format

```text
Setup status: ready | ready except credentials | blocked
Project dir:
Python:
Install:
Provider:
Required key:
Key status: present | missing | not required
Key value: not displayed
Next step:
```

Do not paste raw helper output as the final answer.

## References

- Helper commands and check-only mode: `references/helper-commands.md`
- Provider keys and allowed `.env` settings: `references/provider-env.md`
- Verification checks: `references/verification.md`
