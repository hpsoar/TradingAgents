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

### 1. Use the helper as the source of truth

- Use `python skills/tradingagents-setup/scripts/setup_tradingagents.py ...` for diagnosis, setup, and verification.
- The helper owns cloning, checkout, `.env` creation, data directory creation, dependency installation, and import checks.
- Default target: `~/.tradingagents/source/TradingAgents`.
- Default clone source/ref: `git@github.com:hpsoar/TradingAgents.git` at `v1.0`.
- Override source/ref only when the user explicitly asks, using `--repo-url`, `--ref`, `TRADINGAGENTS_REPO_URL`, or `TRADINGAGENTS_REPO_REF`.
- Use manual shell checks only to diagnose a helper failure.

### 2. Diagnose

For check-only or troubleshooting requests:

```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py --check-only
```

- Summarize project dir, repo action, Python, install/import status, env file, data directories, provider, and credential warning.
- Do not describe check-only as setup; it does not install or write files.

### 3. Set up

- For setup requests, run the helper without `--check-only`.
- Pass user-requested non-secret options through helper flags: `--provider`, `--deep-model`, `--quick-model`, `--backend-url`, `--output-language`, `--venv`, `--china-extra`, `--cache-dir`, `--results-dir`, `--memory-log`, `--repo-url`, and `--ref`.
- If the helper exits with an error or warning, stop and report the specific blocker.
- For later provider/model changes after setup is complete, use `tradingagents-llm`.

### 4. Verify

After setup, rerun check-only:

```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py --check-only
```

- Report `ready` when check-only passes.
- Report `ready except credentials` when only the provider credential is missing.
- Report `blocked` when the helper reports any other blocker.
- If helper output is ambiguous, use `references/verification.md` for targeted manual checks.

## Allowed Writes

- Only writes performed by `setup_tradingagents.py`: fixed project directory, `.env`, requested venv, default data directories, and dependency installation.
- `.env` writes are limited to known non-secret settings and empty credential placeholders.

Never write real API key values unless they already exist in the user's local environment or files. Never ask the user to paste keys into chat.

## Stop Conditions

- The helper reports a conflicting project directory, unsupported Python, unsupported provider, install failure, or blocked network/package operation.
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

Do not paste raw helper output as the final answer.

## References

- Helper commands and check-only mode: `references/helper-commands.md`
- Provider keys and allowed `.env` settings: `references/provider-env.md`
- Verification checks: `references/verification.md`
