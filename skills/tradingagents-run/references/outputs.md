# Outputs

Common output locations:

- Interactive/API logs: `${results_dir}/${symbol}/TradingAgentsStrategy_logs/full_states_log_${analysis_date}.json`
- Interactive saved reports: chosen save directory with `complete_report.md` and section files
- Task runner output: `result.json`, with `analysis_summary`, `decision`, and `artifacts`

When reporting results, include:

- Run status
- Final decision
- Result file
- Report files
- Short summary

Failure categories:

- Validation errors: bad JSON, invalid date, missing symbol, unsupported analyst, or unwritable `output_dir`
- Configuration/model errors: missing API key, provider mismatch, bad model name, or invalid backend URL
- Data unavailable errors: transient vendor issue or unsupported ticker

If a run is expensive, reduce `analysts` first, then reduce `research_depth`.
