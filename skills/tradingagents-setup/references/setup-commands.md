# Setup Commands

```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py --help
```

## Flags

| Flag | Purpose |
|---|---|
| `--provider <name>` | Set default LLM provider |
| `--deep-model <name>` | Model for deep-thinking agents |
| `--quick-model <name>` | Model for quick-thinking agents |
| `--backend-url <url>` | Custom API endpoint or Ollama base URL |
| `--output-language <lang>` | Report language: English or Chinese |
| `--cache-dir <path>` | Cache directory (default: ~/.tradingagents/cache) |
| `--results-dir <path>` | Results directory (default: ~/.tradingagents/logs) |
| `--memory-log <path>` | Memory log path (default: ~/.tradingagents/memory/trading_memory.md) |
| `--china-extra` | Install China market deps (akshare, baostock, tushare) |
| `--venv <path>` | Path for virtual environment |
| `--upgrade-pip` | Upgrade pip before install |
| `--repo-url <url>` | Git repo to clone when no checkout exists |
| `--ref <branch>` | Branch/tag/commit to checkout after clone (default: v1.0) |
| `--check-only` | Only check readiness, no writes |

## Clone target

When no checkout is found, the script clones to:

```
~/.tradingagents/source/TradingAgents
```

After a fresh clone, `cd ~/.tradingagents/source/TradingAgents` to work from the project root.

## Examples

### From scratch (no code yet)
```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py \
  --repo-url git@github.com:hpsoar/TradingAgents.git \
  --ref v1.0 \
  --provider openai
```

### Minimal (already checked out)
```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py --provider openai
```

### Full setup with China market
```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py \
  --provider qwen-cn \
  --deep-model qwen-max \
  --quick-model qwen-plus \
  --output-language Chinese \
  --china-extra
```

### Check only (diagnose)
```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py --check-only
```

Do NOT describe `--check-only` output as a completed setup.
