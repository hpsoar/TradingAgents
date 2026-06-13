"""Internal result models for China market providers."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SourceAttempt:
    provider: str
    status: str
    reason: str = ""


@dataclass
class DataResult:
    kind: str
    symbol: str
    status: str
    provider: str | None = None
    data: Any = None
    message: str = ""
    attempts: list[SourceAttempt] = field(default_factory=list)

    @property
    def usable(self) -> bool:
        return self.status in {"success", "partial"} and self.data is not None

    @classmethod
    def unavailable(
        cls,
        kind: str,
        symbol: str,
        message: str,
        attempts: list[SourceAttempt] | None = None,
    ) -> "DataResult":
        return cls(
            kind=kind,
            symbol=symbol,
            status="unavailable",
            message=message,
            attempts=attempts or [],
        )
