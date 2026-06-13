"""Format China market results for existing TradingAgents tools."""

from __future__ import annotations

from typing import Any

from china_market.models import DataResult


def format_result(result: DataResult) -> str:
    header = [
        f"China A-share data for {result.symbol}",
        f"status: {result.status}",
        f"data_type: {result.kind}",
    ]
    if result.provider:
        header.append(f"source_used: {result.provider}")
    if result.message:
        header.append(f"note: {result.message}")
    if result.attempts:
        attempts = "; ".join(
            f"{a.provider}:{a.status}{f'({a.reason})' if a.reason else ''}"
            for a in result.attempts
        )
        header.append(f"source_attempts: {attempts}")

    body = _format_payload(result.data)
    if not body:
        body = (
            "NO_DATA_AVAILABLE: China market data is unavailable for this request. "
            "Do not estimate or fabricate values; report the missing data and reason."
        )
    return "\n".join(header) + "\n\n" + body


def _format_payload(data: Any) -> str:
    if data is None:
        return ""
    if hasattr(data, "empty") and hasattr(data, "to_string"):
        if data.empty:
            return ""
        return data.head(30).to_string(index=False)
    if isinstance(data, list):
        if not data:
            return ""
        lines = []
        for idx, row in enumerate(data[:30], start=1):
            if isinstance(row, dict):
                values = ", ".join(f"{k}={v}" for k, v in row.items())
                lines.append(f"{idx}. {values}")
            else:
                lines.append(f"{idx}. {row}")
        return "\n".join(lines)
    if isinstance(data, dict):
        return "\n".join(f"{k}: {v}" for k, v in data.items())
    return str(data)
