# Verification

After setup, verify exactly what setup created or changed.

Dependencies:

```bash
cd ~/.tradingagents/source/TradingAgents
python -c "import tradingagents; import cli"
```

CLI entry points:

```bash
cd ~/.tradingagents/source/TradingAgents
python -m cli.main --help
python -m extensions.run.cli --help
```

Config and data directories:

```bash
cd ~/.tradingagents/source/TradingAgents
test -f .env
test -d ~/.tradingagents/cache
test -d ~/.tradingagents/logs
test -d ~/.tradingagents/memory
```

Do not run a full trading analysis as a setup check unless the user explicitly approves external API calls and token usage.
