from __future__ import annotations

from typing import Any

from extensions.run.schema import ErrorInfo, TaskStatus


class RunnerError(Exception):
    """Base for all runner-domain exceptions."""

    status: TaskStatus
    code: str
    retryable: bool

    def __init__(
        self,
        message: str,
        *,
        code: str = "",
        retryable: bool = False,
        details: dict[str, Any] | None = None,
    ):
        super().__init__(message)
        self.code = code or self._default_code()
        self.retryable = retryable
        self.details = details or {}

    def _default_code(self) -> str:
        return "runner_error"

    def to_error_info(self) -> ErrorInfo:
        return ErrorInfo(
            code=self.code,
            message=str(self),
            retryable=self.retryable,
            details=self.details,
        )


class TaskValidationError(RunnerError):
    status = TaskStatus.VALIDATION_ERROR

    def _default_code(self) -> str:
        return "validation_error"


class ConfigurationError(RunnerError):
    status = TaskStatus.CONFIGURATION_ERROR

    def _default_code(self) -> str:
        return "configuration_error"


class DataUnavailableError(RunnerError):
    status = TaskStatus.DATA_UNAVAILABLE

    def _default_code(self) -> str:
        return "data_unavailable"


class ModelError(RunnerError):
    status = TaskStatus.MODEL_ERROR

    def _default_code(self) -> str:
        return "model_error"


class InternalError(RunnerError):
    status = TaskStatus.INTERNAL_ERROR

    def _default_code(self) -> str:
        return "internal_error"


def classify_error(exc: Exception) -> tuple[TaskStatus, ErrorInfo]:
    if isinstance(exc, RunnerError):
        return exc.status, exc.to_error_info()

    msg = str(exc) or type(exc).__name__
    exc_name = type(exc).__name__

    if exc_name in ("ValidationError",):
        return TaskStatus.VALIDATION_ERROR, ErrorInfo(
            code="validation_error", message=msg, retryable=False,
        )

    if exc_name in ("KeyError", "ValueError", "TypeError"):
        return TaskStatus.CONFIGURATION_ERROR, ErrorInfo(
            code="configuration_error", message=msg,
        )

    if "api" in exc_name.lower() or "auth" in exc_name.lower():
        return TaskStatus.CONFIGURATION_ERROR, ErrorInfo(
            code="configuration_error", message=msg, retryable=False,
        )

    exc_str = str(exc).lower()
    if any(k in exc_str for k in ("rate_limit", "timeout", "429", "503")):
        return TaskStatus.MODEL_ERROR, ErrorInfo(
            code="model_error", message=msg, retryable=True,
        )

    if any(k in exc_str for k in ("data", "not found", "no data", "symbol", "ticker")):
        return TaskStatus.DATA_UNAVAILABLE, ErrorInfo(
            code="data_unavailable", message=msg,
        )

    return TaskStatus.INTERNAL_ERROR, ErrorInfo(
        code="internal_error", message=msg,
    )
