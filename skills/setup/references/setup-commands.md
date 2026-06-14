# Setup Commands

Standard setup (from project root):

```bash
python skills/setup/scripts/setup_tradingagents.py --provider openai --deep-model gpt-5.5 --quick-model gpt-5.4-mini
```

With isolated virtual environment:

```bash
python skills/setup/scripts/setup_tradingagents.py --venv .venv --provider openai
```

China market dependencies:

```bash
python skills/setup/scripts/setup_tradingagents.py --china-extra --provider qwen-cn
```

Diagnosis only (no writes):

```bash
python skills/setup/scripts/setup_tradingagents.py --check-only
```

Do not describe `--check-only` output as completed setup — it skips all writes and installs.
