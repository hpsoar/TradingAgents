"""Query China A-share market data.

Usage:
  python scripts/query.py verify
  python scripts/query.py market-data <SYMBOL> [START_DATE] [END_DATE]
  python scripts/query.py company-info <SYMBOL>
  python scripts/query.py financials <SYMBOL>
  python scripts/query.py news <SYMBOL> [START_DATE] [END_DATE] [LIMIT]
  python scripts/query.py indicators <SYMBOL> <INDICATOR> [CURR_DATE] [LOOKBACK_DAYS]
"""

import sys
from datetime import datetime, timedelta

try:
    from china_market.manager import ChinaDataSourceManager
except ImportError:
    print("CHINA_IMPORT_FAILED")
    print("china_market module not available. Install with: pip install tradingagents[china]")
    sys.exit(1)


def default_end() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def default_start() -> str:
    return (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")


def cmd_verify():
    print("CHINA_OK")


def cmd_market_data(args):
    symbol = args[0]
    start = args[1] if len(args) > 1 else default_start()
    end = args[2] if len(args) > 2 else default_end()
    mgr = ChinaDataSourceManager()
    print(mgr.get_market_data(symbol, start, end))


def cmd_company_info(args):
    symbol = args[0]
    mgr = ChinaDataSourceManager()
    print(mgr.get_company_info(symbol))


def cmd_financials(args):
    symbol = args[0]
    mgr = ChinaDataSourceManager()
    print(mgr.get_financial_info(symbol))


def cmd_news(args):
    symbol = args[0]
    start = args[1] if len(args) > 1 else default_start()
    end = args[2] if len(args) > 2 else default_end()
    limit = int(args[3]) if len(args) > 3 else 10
    mgr = ChinaDataSourceManager()
    print(mgr.get_news_events(symbol, start, end, limit))


def cmd_indicators(args):
    symbol = args[0]
    indicator = args[1]
    curr_date = args[2] if len(args) > 2 else default_end()
    lookback = int(args[3]) if len(args) > 3 else 30
    mgr = ChinaDataSourceManager()
    print(mgr.get_indicators(symbol, indicator, curr_date, lookback))


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/query.py <command> [args...]")
        print("Commands: verify, market-data, company-info, financials, news, indicators")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    commands = {
        "verify": cmd_verify,
        "market-data": cmd_market_data,
        "company-info": cmd_company_info,
        "financials": cmd_financials,
        "news": cmd_news,
        "indicators": cmd_indicators,
    }

    fn = commands.get(command)
    if fn is None:
        print(f"Unknown command: {command}")
        print("Commands: verify, market-data, company-info, financials, news, indicators")
        sys.exit(1)

    fn(args)


if __name__ == "__main__":
    main()
