from __future__ import annotations

import os
import re
from datetime import date, datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator


_DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_SUPPORTED_SCHEMA_VERSIONS = {"1.0"}
_DEFAULT_ANALYSTS = ["market", "social", "news", "fundamentals"]


class TaskStatus(str, Enum):
    SUCCESS = "success"
    VALIDATION_ERROR = "validation_error"
    CONFIGURATION_ERROR = "configuration_error"
    DATA_UNAVAILABLE = "data_unavailable"
    MODEL_ERROR = "model_error"
    INTERNAL_ERROR = "internal_error"


class ErrorInfo(BaseModel):
    code: str
    message: str
    retryable: bool = False
    details: dict[str, Any] = Field(default_factory=dict)


class TaskInput(BaseModel):
    schema_version: str = "1.0"
    task_id: str
    symbol: str
    analysis_date: str
    output_dir: str

    asset_type: str = "stock"
    analysts: list[str] = Field(default_factory=lambda: _DEFAULT_ANALYSTS.copy())
    llm_provider: str | None = None
    deep_think_llm: str | None = None
    quick_think_llm: str | None = None
    backend_url: str | None = None
    research_depth: int = 1
    output_language: str = "English"
    checkpoint_enabled: bool = False

    @field_validator("schema_version")
    @classmethod
    def _check_schema_version(cls, v: str) -> str:
        if v not in _SUPPORTED_SCHEMA_VERSIONS:
            msg = f"Unsupported schema_version '{v}'; supported: {_SUPPORTED_SCHEMA_VERSIONS}"
            raise ValueError(msg)
        return v

    @field_validator("task_id")
    @classmethod
    def _check_task_id(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("task_id must not be empty")
        return v.strip()

    @field_validator("symbol")
    @classmethod
    def _check_symbol(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("symbol must not be empty")
        return v.strip().upper()

    @field_validator("analysis_date")
    @classmethod
    def _check_date(cls, v: str) -> str:
        if not _DATE_RE.match(v):
            raise ValueError(f"analysis_date must be YYYY-MM-DD, got '{v}'")
        try:
            datetime.strptime(v, "%Y-%m-%d")
        except ValueError:
            raise ValueError(f"Invalid date: '{v}'")
        return v

    @field_validator("output_dir")
    @classmethod
    def _check_output_dir(cls, v: str) -> str:
        p = Path(v)
        if not p.exists():
            p.mkdir(parents=True, exist_ok=True)
        if not os.access(str(p), os.W_OK):
            raise ValueError(f"output_dir is not writable: '{v}'")
        return str(p.resolve())

    @field_validator("research_depth")
    @classmethod
    def _check_research_depth(cls, v: int) -> int:
        if v < 1:
            return 1
        if v > 10:
            return 10
        return v


class ResultOutput(BaseModel):
    schema_version: str = "1.0"
    task_id: str
    input_summary: dict[str, Any]
    status: TaskStatus
    decision: str | None = None
    analysis_summary: dict[str, str] = Field(default_factory=dict)
    artifacts: dict[str, str] = Field(default_factory=dict)
    error: ErrorInfo | None = None
    started_at: str
    finished_at: str


def build_input_summary(task: TaskInput) -> dict[str, Any]:
    return {
        "schema_version": task.schema_version,
        "task_id": task.task_id,
        "symbol": task.symbol,
        "analysis_date": task.analysis_date,
        "asset_type": task.asset_type,
        "analysts": task.analysts,
        "research_depth": task.research_depth,
        "output_language": task.output_language,
        "checkpoint_enabled": task.checkpoint_enabled,
    }


def build_result(
    task: TaskInput,
    status: TaskStatus,
    *,
    decision: str | None = None,
    final_state: dict[str, Any] | None = None,
    error: ErrorInfo | None = None,
    started_at: str | None = None,
    finished_at: str | None = None,
) -> ResultOutput:
    now = datetime.now(timezone.utc).isoformat()
    input_summary = build_input_summary(task)

    analysis_summary: dict[str, str] = {}
    if final_state:
        for key in ("market_report", "sentiment_report", "news_report", "fundamentals_report",
                     "investment_plan", "trader_investment_plan", "final_trade_decision"):
            if final_state.get(key):
                analysis_summary[key] = final_state[key]

    artifacts: dict[str, str] = {}
    output_dir = Path(task.output_dir)
    result_path = output_dir / "result.json"
    artifacts["result.json"] = str(result_path)

    return ResultOutput(
        schema_version=task.schema_version,
        task_id=task.task_id,
        input_summary=input_summary,
        status=status,
        decision=decision,
        analysis_summary=analysis_summary,
        artifacts=artifacts,
        error=error,
        started_at=started_at or now,
        finished_at=finished_at or now,
    )
