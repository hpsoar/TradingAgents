# Verification

## Priority: use the setup script

```bash
python skills/tradingagents-setup/scripts/setup_tradingagents.py --check-only
```

Use manual checks only when that output is unclear.

## Manual checks

### Dependencies
```bash
python -c "import tradingagents; print('ok')"
```

### CLI entry points
```bash
python -m cli.main --help
python -m extensions.run.cli --help
```

### Confirm repo location
```bash
test -d ~/.tradingagents/source/TradingAgents && echo "repo found"
```

### Config and data directories
```bash
test -f .env && echo ".env exists"
test -d ~/.tradingagents/cache && echo "cache dir exists"
test -d ~/.tradingagents/logs && echo "logs dir exists"
test -d ~/.tradingagents/memory && echo "memory dir exists"
```

Do NOT run a full analysis as a verification check.
