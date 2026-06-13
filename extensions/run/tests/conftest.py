import json
import os
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def _dummy_api_keys(monkeypatch):
    for env_var in (
        "OPENAI_API_KEY", "GOOGLE_API_KEY", "ANTHROPIC_API_KEY",
        "XAI_API_KEY", "DEEPSEEK_API_KEY",
    ):
        monkeypatch.setenv(env_var, os.environ.get(env_var, "placeholder"))


@pytest.fixture()
def tmp_output():
    with tempfile.TemporaryDirectory() as d:
        yield Path(d)


@pytest.fixture()
def valid_task_dict(tmp_output):
    return {
        "schema_version": "1.0",
        "task_id": "test-001",
        "symbol": "AAPL",
        "analysis_date": "2024-05-10",
        "output_dir": str(tmp_output),
    }


@pytest.fixture()
def valid_task_file(tmp_output, valid_task_dict):
    path = tmp_output / "task.json"
    path.write_text(json.dumps(valid_task_dict), encoding="utf-8")
    yield path


@pytest.fixture()
def mock_graph():
    with patch("extensions.run.runner.TradingAgentsGraph") as m:
        instance = MagicMock()
        instance.propagate.return_value = (
            {
                "market_report": "Market is bullish",
                "sentiment_report": "Sentiment positive",
                "final_trade_decision": "Rating: Buy\nBuy the stock.",
            },
            "Buy",
        )
        m.return_value = instance
        yield m
