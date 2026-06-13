# Helper Commands

Use these commands when preparing a TradingAgents environment.

From the fixed TradingAgents project directory:

```bash
cd ~/.tradingagents/source/TradingAgents
python skills/tradingagents-setup/scripts/setup_tradingagents.py --provider openai --deep-model gpt-5.5 --quick-model gpt-5.4-mini
```

With an isolated virtual environment:

```bash
cd ~/.tradingagents/source/TradingAgents
python skills/tradingagents-setup/scripts/setup_tradingagents.py --venv .venv --provider openai
```

For China market dependencies:

```bash
cd ~/.tradingagents/source/TradingAgents
python skills/tradingagents-setup/scripts/setup_tradingagents.py --china-extra --provider qwen-cn
```

From outside the fixed project directory:

```bash
python /path/to/skills/tradingagents-setup/scripts/setup_tradingagents.py --provider openai
```

For diagnosis only, use check-only. Do not describe check-only as completed setup because it skips writes and installs.

```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py --check-only
```
