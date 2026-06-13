#!/usr/bin/env python3
"""Prepare a TradingAgents checkout for local use without storing secrets."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path


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

DEFAULT_REPO_URL = os.environ.get("TRADINGAGENTS_REPO_URL", "git@github.com:hpsoar/TradingAgents.git")
DEFAULT_REPO_REF = os.environ.get("TRADINGAGENTS_REPO_REF", "v1.0")
DEFAULT_PROJECT_DIR = Path.home() / ".tradingagents" / "source" / "TradingAgents"

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


def is_repo_checkout(path: Path) -> bool:
    return (path / "pyproject.toml").exists() and (path / "tradingagents").is_dir()


def ensure_repo_checkout(args: argparse.Namespace) -> tuple[Path, bool, str]:
    if args.install == "package":
        return (Path.home() / ".tradingagents" / "package-run").resolve(), False, "package-only project dir"

    project_dir = DEFAULT_PROJECT_DIR.resolve()
    if is_repo_checkout(project_dir):
        return project_dir, True, "existing repo checkout"

    if project_dir.exists() and any(project_dir.iterdir()):
        raise RuntimeError(
            f"{project_dir} exists but is not a TradingAgents repo checkout. "
            "Move it aside or make it an empty directory before running setup again."
        )

    repo_url = args.repo_url or DEFAULT_REPO_URL
    repo_ref = args.ref or DEFAULT_REPO_REF
    if args.check_only:
        return project_dir, True, f"would clone {repo_url} and checkout {repo_ref}"

    project_dir.parent.mkdir(parents=True, exist_ok=True)
    subprocess.check_call(["git", "clone", repo_url, str(project_dir)])
    if repo_ref:
        subprocess.check_call(["git", "-C", str(project_dir), "checkout", repo_ref])
    return project_dir, True, f"cloned {repo_url} and checked out {repo_ref}"


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


def ensure_env(repo_root: Path, updates: dict[str, str], check_only: bool) -> Path:
    env_path = repo_root / ".env"
    example_path = repo_root / ".env.example"
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
        updates["TRADINGAGENTS_LLM_PROVIDER"] = canonical_provider(args.provider)
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


def provider_key_status(provider: str | None, env_values: dict[str, str]) -> str | None:
    if not provider:
        return "No provider selected. Set TRADINGAGENTS_LLM_PROVIDER or pass --provider."
    provider = canonical_provider(provider)
    key = PROVIDER_KEYS.get(provider)
    if key is None:
        if provider == "ollama":
            return None
        return f"Unknown provider '{provider}'. Known providers: {', '.join(sorted(PROVIDER_KEYS))}."
    if os.environ.get(key) or env_values.get(key):
        return None
    return f"Missing {key} for provider '{provider}'. Add it to .env or the process environment."


def canonical_provider(provider: str) -> str:
    return PROVIDER_ALIASES.get(provider, provider)


def venv_python(venv_dir: Path) -> Path:
    if os.name == "nt":
        return venv_dir / "Scripts" / "python.exe"
    return venv_dir / "bin" / "python"


def ensure_venv(venv_dir: Path, check_only: bool) -> Path:
    python = venv_python(venv_dir)
    if not python.exists() and not check_only:
        subprocess.check_call([sys.executable, "-m", "venv", str(venv_dir)])
    return python


def selected_python(args: argparse.Namespace) -> Path:
    if args.venv:
        return venv_python(Path(args.venv).expanduser())
    return Path(sys.executable)


def install_tradingagents(
    args: argparse.Namespace,
    project_dir: Path,
    is_repo_checkout: bool,
    python: Path,
) -> str:
    mode = args.install
    if mode == "auto":
        if not is_repo_checkout:
            raise RuntimeError(
                "full project setup requires a TradingAgents repo checkout. "
                "Use --install package only when you intentionally want package-only setup."
            )
        mode = "local"
    if mode == "skip":
        return "skipped"
    if mode == "local" and not is_repo_checkout:
        raise RuntimeError("local install requires a TradingAgents repo checkout; use --install package instead.")
    if args.check_only:
        return f"would install {mode} (check-only)"

    if args.upgrade_pip:
        subprocess.check_call([str(python), "-m", "pip", "install", "--upgrade", "pip"])

    if mode == "local":
        spec = ".[china]" if args.china_extra else "."
        command = [str(python), "-m", "pip", "install", "-e", spec]
        subprocess.check_call(command, cwd=project_dir)
        return f"local editable ({spec})"

    spec = "tradingagents[china]" if args.china_extra else "tradingagents"
    subprocess.check_call([str(python), "-m", "pip", "install", spec])
    return f"package ({spec})"


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
    parser = argparse.ArgumentParser(description="Prepare and check a TradingAgents local setup.")
    provider_choices = sorted(set(PROVIDER_KEYS) | set(PROVIDER_ALIASES))
    parser.add_argument("--provider", choices=provider_choices, help="LLM provider to configure.")
    parser.add_argument("--deep-model", help="Model for deep-thinking agents.")
    parser.add_argument("--quick-model", help="Model for quick-thinking agents.")
    parser.add_argument("--backend-url", help="Provider backend URL or Ollama base URL.")
    parser.add_argument("--output-language", help="Report output language, for example English or Chinese.")
    parser.add_argument("--cache-dir", help="Override TRADINGAGENTS_CACHE_DIR.")
    parser.add_argument("--results-dir", help="Override TRADINGAGENTS_RESULTS_DIR.")
    parser.add_argument("--memory-log", help="Override TRADINGAGENTS_MEMORY_LOG_PATH.")
    parser.add_argument(
        "--install",
        choices=("auto", "local", "package", "skip"),
        default="auto",
        help="Install TradingAgents dependencies. auto requires a repo checkout and uses local editable install.",
    )
    parser.add_argument("--china-extra", action="store_true", help="Install the optional China market dependencies.")
    parser.add_argument("--venv", help="Create/use this virtual environment for installation and import checks.")
    parser.add_argument("--upgrade-pip", action="store_true", help="Upgrade pip before installing.")
    parser.add_argument("--repo-url", help=f"Repository URL to clone when no checkout exists. Default: {DEFAULT_REPO_URL}")
    parser.add_argument("--ref", help=f"Branch, tag, or commit to checkout after clone. Default: {DEFAULT_REPO_REF}")
    parser.add_argument("--check-only", action="store_true", help="Report readiness without writing files.")
    args = parser.parse_args()

    try:
        project_dir, is_repo_checkout, repo_action = ensure_repo_checkout(args)
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: Repo checkout failed: {exc}", file=sys.stderr)
        return 2
    if sys.version_info < (3, 10):
        print("ERROR: Python 3.10 or newer is required.", file=sys.stderr)
        return 2
    if not args.check_only:
        project_dir.mkdir(parents=True, exist_ok=True)

    if args.venv:
        python = ensure_venv(Path(args.venv).expanduser(), args.check_only)
    else:
        python = selected_python(args)
    if not python.exists():
        print(f"ERROR: Python executable does not exist: {python}", file=sys.stderr)
        return 2

    updates = build_updates(args)
    env_path = ensure_env(project_dir, updates, args.check_only)
    directories = ensure_directories(args, args.check_only)
    try:
        install_result = install_tradingagents(args, project_dir, is_repo_checkout, python)
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"ERROR: Install failed: {exc}", file=sys.stderr)
        return 2
    env_values = parse_env(env_path)
    provider = args.provider or env_values.get("TRADINGAGENTS_LLM_PROVIDER") or os.environ.get("TRADINGAGENTS_LLM_PROVIDER")
    if provider:
        provider = canonical_provider(provider)
    warning = provider_key_status(provider, env_values)
    planned_clone = args.check_only and repo_action.startswith("would clone ")
    modules = ["tradingagents"]
    if is_repo_checkout or args.install in ("auto", "local"):
        modules.extend(["cli", "china_market"])
    if planned_clone:
        import_check = "not checked (repo would be cloned)"
    else:
        import_check = import_status(python, modules)

    print(f"Project dir: {project_dir}")
    repo_checkout_status = "planned" if planned_clone else ("yes" if is_repo_checkout else "no")
    print(f"Repo checkout: {repo_checkout_status}")
    print(f"Repo action: {repo_action}")
    print(f"Python: {sys.version.split()[0]}")
    print(f"Setup Python: {python}")
    print(f"Install: {install_result}")
    print(f"Import modules ({', '.join(modules)}): {import_check}")
    print(f"Env file: {env_path} ({'exists' if env_path.exists() else 'missing'})")
    for directory in directories:
        print(f"Directory: {directory} ({'exists' if directory.exists() else 'missing'})")
    if provider:
        print(f"Provider: {provider}")
    if warning:
        print(f"WARNING: {warning}", file=sys.stderr)
        return 1
    if import_check != "ok" and not planned_clone:
        print("WARNING: required TradingAgents modules are not importable in the selected Python environment.", file=sys.stderr)
        return 1
    print("TradingAgents setup check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
