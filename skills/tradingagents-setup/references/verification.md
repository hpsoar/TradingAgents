# Verification

After setup, verify the CLI starts:

```bash
tradingagents --help
```

From a source checkout, this direct form also works:

```bash
python -m cli.main --help
```

Also verify that imports work:

```bash
python -c "import tradingagents; import cli"
```

Do not run a full trading analysis as a setup check unless the user explicitly approves external API calls and token usage.
