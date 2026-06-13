# Helper Commands

Use these commands when preparing a TradingAgents environment.

Default clone target:

```text
directory: ~/.tradingagents/source/TradingAgents
repo:      git@github.com:hpsoar/TradingAgents.git
ref:       v1.0
```

Override the source only when the user asks, using `TRADINGAGENTS_REPO_URL`, `TRADINGAGENTS_REPO_REF`, `--repo-url`, or `--ref`.

Standard setup:

```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py --provider openai --deep-model gpt-5.5 --quick-model gpt-5.4-mini
```

With an isolated virtual environment:

```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py --venv .venv --provider openai
```

For China market dependencies:

```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py --china-extra --provider qwen-cn
```

From outside the fixed project directory:

```bash
python /path/to/skills/tradingagents-setup/scripts/setup_tradingagents.py --provider openai
```

With an explicit repository override:

```bash
python /path/to/skills/tradingagents-setup/scripts/setup_tradingagents.py --repo-url git@github.com:hpsoar/TradingAgents.git --ref v1.0 --provider openai
```

For diagnosis only, use check-only. Do not describe check-only as completed setup because it skips writes and installs.

```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py --check-only
```
