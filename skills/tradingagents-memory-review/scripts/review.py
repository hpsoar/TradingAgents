"""Review TradingMemoryLog entries.

Usage:
  python scripts/review.py list-all
  python scripts/review.py filter-ticker <TICKER>
  python scripts/review.py pending
  python scripts/review.py past-context <TICKER> [N_SAME] [N_CROSS]
"""

import sys
import os

PROJECT_DIR = None
stamp_path = os.path.expanduser("~/.tradingagents/.setup_done")
try:
    with open(stamp_path) as f:
        PROJECT_DIR = f.read().strip()
except Exception:
    pass

if PROJECT_DIR:
    sys.path.insert(0, PROJECT_DIR)

try:
    from tradingagents.agents.utils.memory import TradingMemoryLog
except ImportError:
    print("MEMORY_IMPORT_FAILED")
    print("tradingagents module not available. Run tradingagents-setup first.")
    sys.exit(1)


log = TradingMemoryLog()


def cmd_list_all(args=None):
    entries = log.load_entries()
    for e in entries:
        outcome = "pending" if e["pending"] else (e["raw"] or "n/a")
        has_ref = "yes" if e.get("reflection") else "no"
        print(f"[{e['date']} | {e['ticker']} | {e['rating']} | {outcome}]  reflection={has_ref}")
    print(f"Total: {len(entries)} entries")


def cmd_filter_ticker(args):
    ticker = args[0].upper()
    entries = log.load_entries()
    for e in entries:
        if e["ticker"] == ticker:
            outcome = "pending" if e["pending"] else e["raw"]
            print(f"[{e['date']} | {e['rating']} | {outcome}]")
            print(f"DECISION: {e['decision'][:200]}...")
            if e.get("reflection"):
                print(f"REFLECTION: {e['reflection']}")
            print()


def cmd_pending(args=None):
    pending = log.get_pending_entries()
    for e in pending:
        print(f"[{e['date']} | {e['ticker']} | {e['rating']} | pending]")
        print(f"DECISION: {e['decision'][:300]}")
        print()
    print(f"Pending: {len(pending)} entries")


def cmd_past_context(args):
    ticker = args[0].upper()
    n_same = int(args[1]) if len(args) > 1 else 5
    n_cross = int(args[2]) if len(args) > 2 else 3
    ctx = log.get_past_context(ticker, n_same=n_same, n_cross=n_cross)
    print(ctx if ctx else "No past context available.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/review.py <command> [args...]")
        print("Commands: list-all, filter-ticker, pending, past-context")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    commands = {
        "list-all": cmd_list_all,
        "filter-ticker": cmd_filter_ticker,
        "pending": cmd_pending,
        "past-context": cmd_past_context,
    }

    fn = commands.get(command)
    if fn is None:
        print(f"Unknown command: {command}")
        sys.exit(1)

    fn(args)


if __name__ == "__main__":
    main()
