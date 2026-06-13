from __future__ import annotations

import logging
import sys
from pathlib import Path
from typing import Optional

import typer

from extensions.run.errors import RunnerError, TaskValidationError
from extensions.run.schema import TaskStatus
from extensions.run.runner import run_task_file

app = typer.Typer(
    name="ta-run",
    help="Non-interactive TradingAgents analysis runner.",
    no_args_is_help=True,
)

_LEVELS = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
}


@app.command()
def run(
    task: str = typer.Option(
        ...,
        "--task",
        "-t",
        help="Path to the task.json input file.",
        show_default=False,
    ),
    result_file: Optional[str] = typer.Option(
        None,
        "--result-file",
        "-o",
        help="Path for the result.json output (default: <output_dir>/result.json).",
    ),
    log_level: str = typer.Option(
        "info",
        "--log-level",
        "-l",
        help="Logging level: debug, info, warning, error.",
    ),
):
    logging.basicConfig(
        level=_LEVELS.get(log_level.lower(), logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stderr,
    )

    try:
        result = run_task_file(task, result_file)
    except TaskValidationError as exc:
        _fail(exc, exit_code=2)
    except RunnerError as exc:
        _fail(exc, exit_code=1)
    except Exception as exc:
        logging.getLogger("ta_runner").exception("Unexpected error")
        print(f"INTERNAL_ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    if result.status == TaskStatus.SUCCESS:
        print(f"Result written to: {result.artifacts.get('result.json', '?')}", file=sys.stderr)
        sys.exit(0)
    else:
        err = result.error
        msg = f"[{err.code if err else result.status.value}] {err.message if err else ''}"
        print(f"Task failed: {msg}", file=sys.stderr)
        sys.exit(1)


def _fail(exc: RunnerError, exit_code: int) -> None:
    logger = logging.getLogger("ta_runner")
    logger.error("[%s] %s", exc.code, exc)
    if exc.details:
        logger.debug("Details: %s", exc.details)
    print(f"{exc.status.value}: {exc}", file=sys.stderr)
    sys.exit(exit_code)


if __name__ == "__main__":
    app()
