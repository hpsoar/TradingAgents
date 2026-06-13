"""End-to-end analysis for A-share stock using DeepSeek + china_market.

Usage: DEEPSEEK_API_KEY=sk-... uv run python3 run_china_e2e.py
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Ensure we can import china_market
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.dataflows.config import set_config


def main():
    ticker = "600519.SH"
    analysis_date = datetime.now().strftime("%Y-%m-%d")
    output_dir = Path("e2e_output") / ticker / analysis_date
    output_dir.mkdir(parents=True, exist_ok=True)

    # Build config for DeepSeek
    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = "deepseek"
    config["deep_think_llm"] = "deepseek-chat"
    config["quick_think_llm"] = "deepseek-chat"
    config["backend_url"] = "https://api.deepseek.com"
    config["output_language"] = "Chinese"
    config["max_debate_rounds"] = 1
    config["max_risk_discuss_rounds"] = 1
    config["checkpoint_enabled"] = False

    set_config(config)

    # All four analysts
    selected_analysts = ["market", "news", "social", "fundamentals"]

    print(f"[E2E] Initializing TradingAgentsGraph for {ticker}...")
    graph = TradingAgentsGraph(
        selected_analysts=selected_analysts,
        config=config,
        debug=True,
    )

    instrument_context = graph.resolve_instrument_context(ticker, "stock")
    init_state = graph.propagator.create_initial_state(
        ticker,
        analysis_date,
        asset_type="stock",
        instrument_context=instrument_context,
    )
    args = graph.propagator.get_graph_args()

    print(f"[E2E] Starting analysis stream for {ticker} on {analysis_date}...")
    print(f"[E2E] LLM: DeepSeek ({config['deep_think_llm']})\n")
    print("=" * 70)

    reports = {}
    all_messages = []

    for chunk in graph.graph.stream(init_state, **args):
        # Collect reports
        for key in [
            "market_report", "sentiment_report", "news_report",
            "fundamentals_report", "investment_plan",
            "trader_investment_plan", "final_trade_decision",
        ]:
            if chunk.get(key):
                reports[key] = chunk[key]

        # Collect tool calls
        for message in chunk.get("messages", []):
            if hasattr(message, "tool_calls") and message.tool_calls:
                for tc in message.tool_calls:
                    if isinstance(tc, dict):
                        all_messages.append({
                            "type": "tool_call",
                            "name": tc["name"],
                            "args": {k: str(v)[:200] for k, v in tc["args"].items()},
                        })
                    else:
                        all_messages.append({
                            "type": "tool_call",
                            "name": tc.name,
                            "args": {k: str(v)[:200] for k, v in tc.args.items()},
                        })

    print("=" * 70)
    print("\n[E2E] Analysis complete!\n")

    # Summary
    print("=== SECTIONS GENERATED ===")
    for key in [
        "market_report", "sentiment_report", "news_report",
        "fundamentals_report", "investment_plan",
        "trader_investment_plan", "final_trade_decision",
    ]:
        if key in reports:
            content = reports[key]
            text = str(content)[:300]
            print(f"\n--- {key} ---")
            print(text)
            print("...")
        else:
            print(f"\n--- {key} --- [NOT GENERATED]")

    # Tool call summary
    china_calls = [m for m in all_messages if "china" in m["name"].lower() or "china" in str(m["args"]).lower()]
    a_share_calls = [m for m in all_messages if "600519" in str(m["args"]) or "600519.SH" in str(m["args"])]
    print(f"\n\n=== DATA SOURCE ANALYSIS ===")
    print(f"Total tool calls: {len(all_messages)}")
    print(f"Tool calls involving A-share (600519): {len(a_share_calls)}")
    print(f"Tool calls mentioning 'china': {len(china_calls)}")
    print(f"\nAll tool calls:")
    for m in all_messages:
        print(f"  {m['name']}(args={m['args']})")

    # Report which data sources were used
    print(f"\n\n=== DATA SOURCE USAGE ===")
    data_calls = [m for m in all_messages if m["name"] in [
        "get_stock_data", "get_indicators", "get_fundamentals",
        "get_balance_sheet", "get_cashflow", "get_income_statement",
        "get_news", "get_global_news",
    ]]
    for m in data_calls:
        source = "china_market" if "600519" in str(m["args"]) or "000001" in str(m["args"]) else "yfinance/alpha_vantage (existing)"
        print(f"  {m['name']} → {source}")
        print(f"     args: {m['args']}")

    # Save full output to file
    result = {
        "ticker": ticker,
        "analysis_date": analysis_date,
        "llm": {"provider": "deepseek", "model": config["deep_think_llm"]},
        "reports": {k: str(v) for k, v in reports.items()},
        "tool_calls": all_messages,
    }
    out_path = output_dir / "result.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"\n[E2E] Full result saved to {out_path}")


if __name__ == "__main__":
    if not os.environ.get("DEEPSEEK_API_KEY"):
        print("ERROR: DEEPSEEK_API_KEY environment variable is required")
        sys.exit(1)
    main()
