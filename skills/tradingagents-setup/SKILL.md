---
name: tradingagents-setup
description: Set up or diagnose TradingAgents. Use when the user asks to install, configure, verify, or troubleshoot the local TradingAgents environment.
---

# TradingAgents Setup

Prepare a local TradingAgents source checkout for first run without hard-coding, exposing, or inventing user secrets.

## Use When

- Set up TradingAgents for the first time.
- Configure non-secret provider/model defaults.
- Check whether the repo can run.
- Diagnose missing dependencies, `.env`, data directories, or credentials.

## Do Not Use When

- The user wants a package-only install guide.
- The task requires source-code changes, new providers, or model catalog maintenance.

## Default Flow

1. Detect the current state: Python version, repo checkout, `.env`, active/requested virtual environment.
2. Decide setup mode: use the managed checkout at `~/.tradingagents/source/TradingAgents`; reuse it if valid, clone there if missing, and stop if that path conflicts with a non-TradingAgents directory.
3. For check-only requests, diagnose only; do not install dependencies or write files.
4. Configure non-secret settings: create `.env` from `.env.example` if missing and write only requested known overrides.
5. Install dependencies only when setup is requested, using the helper script or equivalent repo install.
6. Create default data directories under `~/.tradingagents` when missing.
7. Verify imports, CLI startup, selected provider, and required credential presence.
8. Report readiness and the next concrete action.

## Allowed Writes

- `.env`, but only for known non-secret `TRADINGAGENTS_*` settings and empty credential placeholders.
- Requested virtual environment directories.
- Default data directories: `~/.tradingagents/cache`, `~/.tradingagents/logs`, `~/.tradingagents/memory`.
- Dependency installation into the selected environment.

Never write real API key values unless they already exist in the user's local environment or files. Never ask the user to paste keys into chat.

## Stop Conditions

- The managed checkout path exists, is non-empty, and is not a TradingAgents repo.
- Python is older than 3.10.
- Required credentials are missing after setup; report the env var instead of running analysis.
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
