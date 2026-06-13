from __future__ import annotations

import json
import logging
import os
import sys
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from tradingagents.default_config import DEFAULT_CONFIG
from tradingagents.graph.trading_graph import TradingAgentsGraph

from extensions.run.errors import (
    ConfigurationError,
    DataUnavailableError,
    InternalError,
    ModelError,
    RunnerError,
    TaskValidationError,
    classify_error,
)
from extensions.run.schema import (
    TaskInput,
    TaskStatus,
    ResultOutput,
    build_result,
)

logger = logging.getLogger("ta_runner")


def _resolve_analysts(task: TaskInput) -> list[str]:
    analysts = task.analysts
    if not analysts:
        return ["market", "social", "news", "fundamentals"]
    return analysts


def _build_config(task: TaskInput) -> dict[str, Any]:
    config = DEFAULT_CONFIG.copy()
    config["results_dir"] = task.output_dir
    data_cache = os.path.join(task.output_dir, ".tradingagents", "cache")
    memory_log = os.path.join(task.output_dir, ".tradingagents", "memory", "trading_memory.md")
    config["data_cache_dir"] = data_cache
    config["memory_log_path"] = memory_log
    if task.llm_provider:
        config["llm_provider"] = task.llm_provider
    if task.deep_think_llm:
        config["deep_think_llm"] = task.deep_think_llm
    if task.quick_think_llm:
        config["quick_think_llm"] = task.quick_think_llm
    if task.backend_url:
        config["backend_url"] = task.backend_url
    config["max_debate_rounds"] = task.research_depth
    config["max_risk_discuss_rounds"] = task.research_depth
    config["output_language"] = task.output_language
    config["checkpoint_enabled"] = task.checkpoint_enabled
    return config


def _run_propagate(
    task: TaskInput,
    config: dict[str, Any],
) -> tuple[dict[str, Any], str]:
    analysts = _resolve_analysts(task)
    graph = TradingAgentsGraph(
        selected_analysts=analysts,
        config=config,
    )
    final_state, decision = graph.propagate(
        task.symbol,
        task.analysis_date,
        asset_type=task.asset_type or "stock",
    )
    return final_state, decision


def run_task(task: TaskInput) -> ResultOutput:
    started_at = datetime.now(timezone.utc).isoformat()
    config = _build_config(task)
    os.makedirs(config["data_cache_dir"], exist_ok=True)
    os.makedirs(os.path.dirname(config["memory_log_path"]), exist_ok=True)

    try:
        final_state, decision = _run_propagate(task, config)
    except RunnerError:
        raise
    except Exception as exc:
        status, error_info = classify_error(exc)
        raise InternalError(
            str(exc),
            code=error_info.code,
            retryable=error_info.retryable,
            details={**error_info.details, "traceback": traceback.format_exc()},
        ) from exc

    finished_at = datetime.now(timezone.utc).isoformat()
    return build_result(
        task=task,
        status=TaskStatus.SUCCESS,
        decision=decision,
        final_state=final_state,
        started_at=started_at,
        finished_at=finished_at,
    )


def run_task_file(task_path: str, result_path: str | None = None) -> ResultOutput:
    task_file = Path(task_path)
    if not task_file.exists():
        raise TaskValidationError(f"Task file not found: {task_path}", code="file_not_found")

    try:
        raw = json.loads(task_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise TaskValidationError(
            f"Invalid JSON in task file: {exc}",
            code="invalid_json",
            details={"path": task_path},
        ) from exc

    try:
        task = TaskInput.model_validate(raw)
    except Exception as exc:
        raise TaskValidationError(
            f"Task validation failed: {exc}",
            code="validation_error",
            details={"path": task_path},
        ) from exc

    result = run_task(task)

    output_path = result_path or os.path.join(task.output_dir, "result.json")
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(
        result.model_dump_json(indent=2, exclude_none=True),
        encoding="utf-8",
    )
    result.artifacts["result.json"] = str(output_file.resolve())

    return result
