#!/usr/bin/env python3
"""Prepare a TradingAgents checkout for local use without storing secrets."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


DEFAULT_REPO_URL = "git@github.com:hpsoar/TradingAgents.git"
DEFAULT_REPO_REF = "v1.0"
DEFAULT_CLONE_DIR = Path.home() / ".tradingagents" / "source" / "TradingAgents"

PROVIDER_KEYS = {
    "openai": "OPENAI_API_KEY",
    "google": "GOOGLE_API_KEY",
    "anthropic": "ANTHROPIC_API_KEY",
    "azure": "AZURE_OPENAI_API_KEY",
    "xai": "XAI_API_KEY",
    "deepseek": "DEEPSEEK_API_KEY",
    "qwen": "DASHSCOPE_API_KEY",
    "qwen-cn": "DASHSCOPE_CN_API_KEY",
    "glm": "ZHIPU_API_KEY",
    "glm-cn": "ZHIPU_CN_API_KEY",
    "minimax": "MINIMAX_API_KEY",
    "minimax-cn": "MINIMAX_CN_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
    "ollama": None,
}

PROVIDER_ALIASES = {
    "dashscope": "qwen",
    "dashscope_cn": "qwen-cn",
    "zhipu": "glm",
    "zhipu_cn": "glm-cn",
    "minimax_cn": "minimax-cn",
}

ENV_TEMPLATE = """# LLM Providers (set the one you use)
OPENAI_API_KEY=
GOOGLE_API_KEY=
ANTHROPIC_API_KEY=
AZURE_OPENAI_API_KEY=
XAI_API_KEY=
DEEPSEEK_API_KEY=
DASHSCOPE_API_KEY=
DASHSCOPE_CN_API_KEY=
ZHIPU_API_KEY=
ZHIPU_CN_API_KEY=
MINIMAX_API_KEY=
MINIMAX_CN_API_KEY=
OPENROUTER_API_KEY=

# Optional data provider key
ALPHA_VANTAGE_API_KEY=

# Optional: point at a remote Ollama server.
#OLLAMA_BASE_URL=http://your-ollama-host:11434/v1

# Optional: override TradingAgents defaults without editing code.
#TRADINGAGENTS_LLM_PROVIDER=openai
#TRADINGAGENTS_DEEP_THINK_LLM=gpt-5.5
#TRADINGAGENTS_QUICK_THINK_LLM=gpt-5.4-mini
#TRADINGAGENTS_LLM_BACKEND_URL=
#TRADINGAGENTS_OUTPUT_LANGUAGE=English
#TRADINGAGENTS_MAX_DEBATE_ROUNDS=1
#TRADINGAGENTS_MAX_RISK_ROUNDS=1
#TRADINGAGENTS_CHECKPOINT_ENABLED=false
#TRADINGAGENTS_TEMPERATURE=0.0
"""


def is_project_root(path: Path) -> bool:
    return (path / "pyproject.toml").exists() and (path / "tradingagents").is_dir()


def find_project_root(args: argparse.Namespace) -> tuple[Path, bool, str]:
    """Find or clone the TradingAgents project root.

    Returns (project_root, is_local, action_description).
    """
    candidates = [
        Path.cwd().resolve(),
        Path(__file__).resolve().parent.parent.parent.parent.resolve(),
        DEFAULT_CLONE_DIR.resolve(),
    ]
    for c in candidates:
        if is_project_root(c):
            return c, True, "existing checkout"

    if args.check_only:
        return DEFAULT_CLONE_DIR, False, f"would clone {args.repo_url} @ {args.ref} to {DEFAULT_CLONE_DIR}"

    project_dir = DEFAULT_CLONE_DIR
    project_dir.parent.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(["git", "clone", args.repo_url, str(project_dir)])
    if args.ref:
        subprocess.check_call(["git", "-C", str(project_dir), "checkout", args.ref])
    return project_dir, True, f"cloned {args.repo_url} @ {args.ref} to {project_dir}"


def parse_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.exists():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key, value = stripped.split("=", 1)
        values[key.strip()] = value.strip().strip('"').strip("'")
    return values


def upsert_env(path: Path, updates: dict[str, str]) -> None:
    existing = path.read_text(encoding="utf-8").splitlines() if path.exists() else []
    seen: set[str] = set()
    next_lines: list[str] = []

    for line in existing:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            next_lines.append(line)
            continue
        key, current = line.split("=", 1)
        key = key.strip()
        if key in updates:
            seen.add(key)
            next_lines.append(line if current.strip() else f"{key}={updates[key]}")
        else:
            next_lines.append(line)

    for key, value in updates.items():
        if key not in seen:
            next_lines.append(f"{key}={value}")

    path.write_text("\n".join(next_lines).rstrip() + "\n", encoding="utf-8")


def ensure_env(project_root: Path, updates: dict[str, str], check_only: bool) -> Path:
    env_path = project_root / ".env"
    example_path = project_root / ".env.example"
    if not env_path.exists() and not check_only:
        if example_path.exists():
            shutil.copyfile(example_path, env_path)
        else:
            env_path.write_text(ENV_TEMPLATE, encoding="utf-8")
    if updates and not check_only:
        upsert_env(env_path, updates)
    return env_path


def ensure_directories(args: argparse.Namespace, check_only: bool) -> list[Path]:
    home = Path.home() / ".tradingagents"
    cache_dir = Path(args.cache_dir).expanduser() if args.cache_dir else home / "cache"
    results_dir = Path(args.results_dir).expanduser() if args.results_dir else home / "logs"
    memory_log = Path(args.memory_log).expanduser() if args.memory_log else home / "memory" / "trading_memory.md"
    directories = [cache_dir, results_dir, memory_log.parent]
    if not check_only:
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    return directories


def build_updates(args: argparse.Namespace) -> dict[str, str]:
    updates: dict[str, str] = {}
    if args.provider:
        updates["TRADINGAGENTS_LLM_PROVIDER"] = _canonical_provider(args.provider)
    if args.deep_model:
        updates["TRADINGAGENTS_DEEP_THINK_LLM"] = args.deep_model
    if args.quick_model:
        updates["TRADINGAGENTS_QUICK_THINK_LLM"] = args.quick_model
    if args.backend_url:
        if args.provider == "ollama":
            updates["OLLAMA_BASE_URL"] = args.backend_url
        else:
            updates["TRADINGAGENTS_LLM_BACKEND_URL"] = args.backend_url
    if args.output_language:
        updates["TRADINGAGENTS_OUTPUT_LANGUAGE"] = args.output_language
    if args.cache_dir:
        updates["TRADINGAGENTS_CACHE_DIR"] = args.cache_dir
    if args.results_dir:
        updates["TRADINGAGENTS_RESULTS_DIR"] = args.results_dir
    if args.memory_log:
        updates["TRADINGAGENTS_MEMORY_LOG_PATH"] = args.memory_log
    return updates


def _canonical_provider(provider: str) -> str:
    return PROVIDER_ALIASES.get(provider, provider)


def provider_key_status(provider: str | None, env_values: dict[str, str]) -> str | None:
    if not provider:
        return "No provider selected. Set TRADINGAGENTS_LLM_PROVIDER or pass --provider."
    provider = _canonical_provider(provider)
    key = PROVIDER_KEYS.get(provider)
    if key is None:
        if provider == "ollama":
            return None
        return f"Unknown provider '{provider}'. Known: {', '.join(sorted(PROVIDER_KEYS))}."
    if os.environ.get(key) or env_values.get(key):
        return None
    return f"Missing {key} for provider '{provider}'. Add it to .env or the process environment."


def venv_python(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def ensure_venv(venv_dir: Path, check_only: bool) -> Path:
    python = venv_python(venv_dir)
    if not python.exists() and not check_only:
        subprocess.check_call([sys.executable, "-m", "venv", str(venv_dir)])
    return python


def install_tradingagents(
    project_root: Path,
    python: Path,
    china_extra: bool,
    upgrade_pip: bool,
    check_only: bool,
) -> str:
    if check_only:
        extras = "[china]" if china_extra else ""
        return f"would install .{extras} (check-only)"

    if upgrade_pip:
        subprocess.check_call([str(python), "-m", "pip", "install", "--upgrade", "pip"])

    spec = ".[china]" if china_extra else "."
    subprocess.check_call([str(python), "-m", "pip", "install", "-e", spec], cwd=project_root)
    return f"editable install ({spec})"


def import_status(python: Path, modules: list[str]) -> str:
    code = "\n".join(f"import {module}" for module in modules) + "\nprint('ok')"
    result = subprocess.run(
        [str(python), "-c", code],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if result.returncode == 0:
        return "ok"
    return result.stderr.strip().splitlines()[-1] if result.stderr.strip() else "failed"


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare a TradingAgents checkout for use.")
    provider_choices = sorted(set(PROVIDER_KEYS) | set(PROVIDER_ALIASES))
    parser.add_argument("--provider", choices=provider_choices, help="Default LLM provider.")
    parser.add_argument("--deep-model", help="Model for deep-thinking agents.")
    parser.add_argument("--quick-model", help="Model for quick-thinking agents.")
    parser.add_argument("--backend-url", help="Provider backend URL or Ollama base URL.")
    parser.add_argument("--output-language", help="Report language, e.g. English or Chinese.")
    parser.add_argument("--cache-dir", help="Override TRADINGAGENTS_CACHE_DIR.")
    parser.add_argument("--results-dir", help="Override TRADINGAGENTS_RESULTS_DIR.")
    parser.add_argument("--memory-log", help="Override TRADINGAGENTS_MEMORY_LOG_PATH.")
    parser.add_argument("--china-extra", action="store_true", help="Install China market dependencies.")
    parser.add_argument("--venv", help="Create/use virtual environment at this path.")
    parser.add_argument("--upgrade-pip", action="store_true", help="Upgrade pip before install.")
    parser.add_argument("--repo-url", default=DEFAULT_REPO_URL, help="Repository URL to clone when no checkout exists.")
    parser.add_argument("--ref", default=DEFAULT_REPO_REF, help="Branch/tag/commit to checkout after clone.")
    parser.add_argument("--check-only", action="store_true", help="Only check readiness, no writes.")
    args = parser.parse_args()

    try:
        project_root, is_local, repo_action = find_project_root(args)
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: Repo clone failed: {exc}", file=sys.stderr)
        return 2

    if sys.version_info < (3, 10):
        print("ERROR: Python 3.10+ required.", file=sys.stderr)
        return 2

    if args.venv:
        python = ensure_venv(Path(args.venv).expanduser(), args.check_only)
    else:
        python = Path(sys.executable)
    if not python.exists():
        print(f"ERROR: Python not found: {python}", file=sys.stderr)
        return 2

    updates = build_updates(args)
    env_path = ensure_env(project_root, updates, args.check_only)
    directories = ensure_directories(args, args.check_only)

    try:
        install_result = install_tradingagents(
            project_root, python, args.china_extra, args.upgrade_pip, args.check_only,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: Install failed: {exc}", file=sys.stderr)
        return 2

    env_values = parse_env(env_path)
    provider = (
        args.provider
        or env_values.get("TRADINGAGENTS_LLM_PROVIDER")
        or os.environ.get("TRADINGAGENTS_LLM_PROVIDER")
    )
    if provider:
        provider = _canonical_provider(provider)

    warning = provider_key_status(provider, env_values)
    modules = ["tradingagents"]
    import_check = import_status(python, modules)

    print(f"Project root: {project_root}")
    print(f"Repo: {repo_action}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Setup Python: {python}")
    print(f"Install: {install_result}")
    print(f"Import tradingagents: {import_check}")
    print(f"Env file: {env_path} ({'exists' if env_path.exists() else 'missing'})")
    for d in directories:
        print(f"Directory: {d} ({'exists' if d.exists() else 'missing'})")
    if provider:
        print(f"Provider: {provider}")
    if warning:
        print(f"WARNING: {warning}", file=sys.stderr)
        return 1
    if import_check != "ok":
        print("WARNING: tradingagents module is not importable.", file=sys.stderr)
        return 1
    print("Setup check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
