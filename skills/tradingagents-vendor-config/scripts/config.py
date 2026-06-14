"""Configure TradingAgents data vendors.

Usage:
  python scripts/config.py show
  python scripts/config.py set-all <VENDOR>
  python scripts/config.py set-category <CATEGORY> <VENDOR>
  python scripts/config.py set-tool <TOOL> <VENDOR>
  python scripts/config.py reset
  python scripts/config.py check-cred <VENDOR>
  python scripts/config.py verify
"""

import sys
import os
import subprocess

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
    from tradingagents.dataflows.config import set_config, get_config
except ImportError:
    print("CONFIG_IMPORT_FAILED")
    print("tradingagents module not available. Run tradingagents-setup first.")
    sys.exit(1)


CATEGORIES = ["core_stock_apis", "technical_indicators", "fundamental_data", "news_data"]
VENDORS = ["yfinance", "alpha_vantage"]


def cmd_show():
    cfg = get_config()
    print("--- Category-level vendors (data_vendors) ---")
    for k in CATEGORIES:
        print(f"  {k}: {cfg.get('data_vendors', {}).get(k, 'not set')}")
    print()
    print("--- Tool-level overrides (tool_vendors) ---")
    tv = cfg.get("tool_vendors", {})
    if tv:
        for k, v in tv.items():
            print(f"  {k}: {v}")
    else:
        print("  (none)")


def cmd_set_all(args):
    vendor = args[0]
    if vendor not in VENDORS:
        print(f"ERROR: Unknown vendor '{vendor}'. Supported: {', '.join(VENDORS)}")
        sys.exit(1)
    set_config({
        "data_vendors": {cat: vendor for cat in CATEGORIES},
        "tool_vendors": {},
    })
    print(f"Set all categories to '{vendor}'.")
    cmd_show()


def cmd_set_category(args):
    category, vendor = args[0], args[1]
    if category not in CATEGORIES:
        print(f"ERROR: Unknown category '{category}'. Supported: {', '.join(CATEGORIES)}")
        sys.exit(1)
    if vendor not in VENDORS:
        print(f"ERROR: Unknown vendor '{vendor}'. Supported: {', '.join(VENDORS)}")
        sys.exit(1)
    set_config({"data_vendors": {category: vendor}})
    print(f"Set '{category}' to '{vendor}'.")
    cmd_show()


def cmd_set_tool(args):
    tool, vendor = args[0], args[1]
    if vendor not in VENDORS:
        print(f"ERROR: Unknown vendor '{vendor}'. Supported: {', '.join(VENDORS)}")
        sys.exit(1)
    set_config({"tool_vendors": {tool: vendor}})
    print(f"Set tool override '{tool}' to '{vendor}'.")
    cmd_show()


def cmd_reset():
    set_config({
        "data_vendors": {cat: "yfinance" for cat in CATEGORIES},
        "tool_vendors": {},
    })
    print("Reset all vendors to yfinance defaults.")
    cmd_show()


def cmd_check_cred(args):
    vendor = args[0]
    if vendor == "alpha_vantage":
        env_var = "ALPHA_VANTAGE_API_KEY"
    else:
        print(f"No credential check needed for '{vendor}'.")
        return
    if PROJECT_DIR and os.path.exists(os.path.join(PROJECT_DIR, ".env")):
        result = subprocess.run(
            ["grep", "-E", f"^{env_var}=", os.path.join(PROJECT_DIR, ".env")],
            capture_output=True, text=True,
        )
        if result.returncode == 0:
            print(f"{env_var}: present")
        else:
            print(f"{env_var}: missing")
            print(f"Alpha Vantage requires {env_var} in .env. Please add it.")
    else:
        print(f"{env_var}: cannot check (.env not found)")


def cmd_verify():
    cmd_show()


def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/config.py <command> [args...]")
        print("Commands: show, set-all, set-category, set-tool, reset, check-cred, verify")
        sys.exit(1)

    command = sys.argv[1]
    args = sys.argv[2:]

    commands = {
        "show": cmd_show,
        "set-all": cmd_set_all,
        "set-category": cmd_set_category,
        "set-tool": cmd_set_tool,
        "reset": cmd_reset,
        "check-cred": cmd_check_cred,
        "verify": cmd_verify,
    }

    fn = commands.get(command)
    if fn is None:
        print(f"Unknown command: {command}")
        print("Commands: show, set-all, set-category, set-tool, reset, check-cred, verify")
        sys.exit(1)

    fn(args)


if __name__ == "__main__":
    main()
