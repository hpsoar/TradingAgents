---
name: tradingagents-setup
description: "Install TradingAgents dependencies, create .env from template, create ~/.tradingagents data directories, and verify the tradingagents module imports. Use when: the user says 'setup', 'install', 'first time', 'get started'; or another skill (tradingagents-run, tradingagents-config) reports a check-only failure; or .env is missing; or the tradingagents module cannot be imported."
allowed-tools: Bash(python *), Bash(pip *), Bash(test *), Bash(ls *), Bash(which *)
---

# TradingAgents Setup

Prepare a TradingAgents checkout so `tradingagents-run` can execute.

## Decision Tree

### Step 1 — Check whether setup is needed

Run:

```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py --check-only
```

Parse the exit code and the last line of stdout:

| Exit code | Last stdout line | Meaning | Next action |
|---|---|---|---|
| 0 | `Setup check passed.` | Already ready | Go to Step 5 |
| 1 | `Setup check passed.` | Ready but stderr has a `WARNING:` | Go to Step 5, report the warning |
| 1 | anything else | Blocked or incomplete | Go to Step 2 |
| 2 | anything | ERROR | Report the error and stop |

Also check stdout for the `Repo:` line. If it says `would clone ...`, the code is not on the machine yet — go to Step 2 to proceed with actual setup (which will clone first).

If exit code is 1 and stderr contains `WARNING: Missing <ENV_VAR>`, report the env var name to the user and say "ready except credentials" — do NOT rerun setup.

### Step 2 — Gather user preferences

Ask the user (or read from conversation context):

| Question | Default | Notes |
|---|---|---|
| LLM provider | `openai` | One of: openai, anthropic, google, azure, xai, deepseek, qwen, qwen-cn, glm, glm-cn, minimax, minimax-cn, openrouter, ollama |
| Deep-think model | `gpt-5.5` | |
| Quick-think model | `gpt-5.4-mini` | |
| Output language | `English` | English or Chinese |
| Use virtual env? | no | If yes, path like `.venv` |
| Install China extras? | no | `--china-extra` for A-share support |

If the code is not on the machine yet (check-only said `would clone`), also ask:
- Which git repo URL to clone from (default: `git@github.com:hpsoar/TradingAgents.git`)
- Which ref to checkout (default: `v1.0`)

Stop if the user does not provide a provider. Report `blocked`.

### Step 3 — Run setup script

A — Basic setup (repo already checked out):

```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py \
  --provider <provider> \
  --deep-model <model> \
  --quick-model <model>
```

B — From scratch (no code on machine yet):

```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py \
  --repo-url git@github.com:hpsoar/TradingAgents.git \
  --ref v1.0 \
  --provider <provider>
```

C — With virtual environment:

```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py \
  --venv .venv \
  --provider <provider>
```

D — With China extras:

```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py \
  --china-extra \
  --provider <provider>
```

E — Custom language and custom data dirs:

```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py \
  --provider <provider> \
  --output-language Chinese
```

### Step 4 — Parse the output

Look for the `Repo:` line in stdout:

| Repo: line | Meaning |
|---|---|
| `Repo: existing checkout` | Code already on disk |
| `Repo: cloned ... to /home/user/.tradingagents/source/TradingAgents` | Freshly cloned |
| `Repo: would clone ...` (check-only) | Code not on disk, clone planned |

Then check the final result:

| stdout or stderr pattern | Meaning | Action |
|---|---|---|
| `Setup check passed.` | Success | Go to Step 5 |
| `WARNING: Missing <ENV_VAR>` | Ready except credentials | Tell user which env var, then done |
| `ERROR: *` | Blocked | Report the exact error, stop |

On any `ERROR`, report the full error line and stop. Do not retry.

If the repo was freshly cloned to `~/.tradingagents/source/TradingAgents`, subsequent skills (run, config) must use that directory — the agent should `cd` there or pass it as context.

On success, setup stamps `~/.tradingagents/.setup_done` with the project root path. This stamp is how `tradingagents-run` and `tradingagents-config` verify setup is complete.

### Step 5 — Report status

```text
Setup status: ready | ready except credentials | blocked
Project root: /home/user/.tradingagents/source/TradingAgents
Setup stamp: ~/.tradingagents/.setup_done (written)
Python: 3.12
Install: editable install (.)
Import tradingagents: ok
Provider: openai
Required key: OPENAI_API_KEY
Key status: present | missing | not required
Next step: Use tradingagents-run to run analysis, or tradingagents-config to change settings.
```

If status is `ready`, the user can now run analysis. If `ready except credentials`, tell them to set the env var.

## Allowed Writes

- `.env` in the project root — only known `TRADINGAGENTS_*` settings and empty credential placeholders.
- `~/.tradingagents/` — cache, logs, memory directories.
- `~/.tradingagents/source/TradingAgents` — git clone when no checkout exists.
- Virtual environment at the requested path.
- Editable pip install of the project.

Never write real API key values.

## Stop Conditions

- Python < 3.10.
- pip install fails with network or permission error.
- git clone fails (bad URL, no network, no auth).
- User refuses to choose a provider.

## References

- `references/setup-commands.md` — full flag reference
- `references/provider-env.md` — provider ↔ env var mapping
- `references/verification.md` — manual check commands
