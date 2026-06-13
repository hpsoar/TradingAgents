---
name: tradingagents-setup
description: Set up or diagnose TradingAgents. Use when the user asks to install, configure, verify, or troubleshoot the local TradingAgents environment.
---

# TradingAgents Setup

Prepare the local TradingAgents environment without hard-coding, exposing, or inventing user secrets.

## Use When

- Set up TradingAgents for the first time.
- Configure initial non-secret provider/model defaults during setup.
- Check whether the TradingAgents project directory can run.
- Diagnose missing dependencies, `.env`, data directories, or credentials.

## Execution Process

### 1. Run diagnosis

Run:

```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py --check-only
```

- If stdout contains `Repo checkout: planned` or starts a line with `Repo action: would clone `, report `blocked`: the project has not been cloned yet.
- If stderr starts with `ERROR:`, report `blocked` with that error.
- If stderr contains `WARNING: Missing <ENV_VAR> for provider`, report `ready except credentials` and name `<ENV_VAR>`.
- If stderr contains any other `WARNING:`, report `blocked` with that warning.
- If exit code is `0` and no planned clone appears in stdout, report `ready`.
- For a check-only request, stop here.

### 2. Run setup

For a setup request, run the setup script without `--check-only`.

```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py
```

- Add requested flags: `--provider`, `--deep-model`, `--quick-model`, `--backend-url`, `--output-language`, `--venv`, `--china-extra`, `--cache-dir`, `--results-dir`, `--memory-log`, `--repo-url`, or `--ref`.
- Use the default clone target/source/ref unless the user asks otherwise: `~/.tradingagents/source/TradingAgents`, `git@github.com:hpsoar/TradingAgents.git`, `v1.0`.
- Interpret stdout/stderr using the same rules from step 1.

### 3. Verify setup

Run diagnosis again:

```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py --check-only
```

- Interpret the result using the same rules from step 1.
- Use `references/verification.md` only when the script output is unclear.

### 4. Route follow-up work

- For later provider/model changes, use `tradingagents-llm`.
- For analysis runs after setup is ready, use `tradingagents-run`.

## Allowed Writes

- Only writes performed by `setup_tradingagents.py`: fixed project directory, `.env`, requested venv, default data directories, and dependency installation.
- `.env` writes are limited to known non-secret settings and empty credential placeholders.

Never write real API key values unless they already exist in the user's local environment or files. Never ask the user to paste keys into chat.

## Stop Conditions

- The setup script reports a conflicting project directory, unsupported Python, unsupported provider, install failure, or blocked network/package operation.
- Required credentials are missing after setup; report the env var and mark readiness as `ready except credentials`.

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

Do not paste raw setup script output as the final answer.

## References

- Setup script commands and check-only mode: `references/setup-commands.md`
- Provider keys and allowed `.env` settings: `references/provider-env.md`
- Verification checks: `references/verification.md`
