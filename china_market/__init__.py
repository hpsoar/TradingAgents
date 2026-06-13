"""China A-share data source extension for TradingAgents.

This package is intentionally isolated from the existing TradingAgents
dataflows.  The public adapter functions return the same string-oriented
payloads existing tools consume, while provider details stay private here.
"""

from .symbols import NormalizedSymbol, normalize_symbol

__all__ = ["NormalizedSymbol", "normalize_symbol"]
