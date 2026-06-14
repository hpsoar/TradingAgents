# Verification

After setup, verify with the setup script first:

```bash
python skills/setup/scripts/setup_tradingagents.py --check-only
```

Use manual checks only when the setup script output is unclear.

Dependencies:

```bash
python -c "import tradingagents; import cli; import china_market"
```

CLI entry points:

```bash
python -m cli.main --help
python -m extensions.run.cli --help
```

Config and data directories:

```bash
test -f .env
test -d ~/.tradingagents/cache
test -d ~/.tradingagents/logs
test -d ~/.tradingagents/memory
```

Do not run a full analysis as a setup check unless the user explicitly approves API calls and token usage.
