"""A-share symbol recognition and normalization."""

from __future__ import annotations

from dataclasses import dataclass
import re


_SH_PREFIXES = ("600", "601", "603", "605", "688", "900")
_SZ_PREFIXES = ("000", "001", "002", "003", "300", "301", "200")


@dataclass(frozen=True)
class NormalizedSymbol:
    """Canonical representation of an A-share symbol."""

    original: str
    code: str
    exchange: str

    @property
    def canonical(self) -> str:
        return f"{self.code}.{self.exchange}"

    @property
    def akshare_symbol(self) -> str:
        return f"{self.exchange.lower()}{self.code}"

    @property
    def tushare_symbol(self) -> str:
        return self.canonical

    @property
    def baostock_symbol(self) -> str:
        return f"{self.exchange.lower()}.{self.code}"


def normalize_symbol(raw: str) -> NormalizedSymbol | None:
    """Return an A-share canonical symbol, or ``None`` for non-A-share input."""

    if not isinstance(raw, str) or not raw.strip():
        return None

    original = raw.strip()
    symbol = original.upper().strip()

    # Do not steal explicit non-A-share exchange formats.
    if symbol.endswith(".HK") or symbol.endswith(".US"):
        return None

    # Normalize Yahoo Finance .SS suffix (used by yfinance for Shanghai)
    # to the canonical .SH exchange code used by Chinese data providers.
    if symbol.endswith(".SS"):
        symbol = symbol[:-3] + ".SH"

    prefixed = re.fullmatch(r"(SH|SZ)\.?(\d{6})", symbol)
    if prefixed:
        exchange, code = prefixed.groups()
        return NormalizedSymbol(original=original, code=code, exchange=exchange)

    suffixed = re.fullmatch(r"(\d{6})\.(SH|SZ)", symbol)
    if suffixed:
        code, exchange = suffixed.groups()
        return NormalizedSymbol(original=original, code=code, exchange=exchange)

    if re.fullmatch(r"\d{6}", symbol):
        exchange = infer_exchange(symbol)
        if exchange:
            return NormalizedSymbol(original=original, code=symbol, exchange=exchange)

    return None


def infer_exchange(code: str) -> str | None:
    """Infer SH/SZ for common six-digit A-share code prefixes."""

    if code.startswith(_SH_PREFIXES):
        return "SH"
    if code.startswith(_SZ_PREFIXES):
        return "SZ"
    return None
