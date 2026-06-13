import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from extensions.run.errors import RunnerError, TaskValidationError, InternalError
from extensions.run.runner import run_task, run_task_file
from extensions.run.schema import TaskInput, TaskStatus


@pytest.mark.unit
class TestRunTask:
    def test_success(self, valid_task_dict, mock_graph):
        task = TaskInput.model_validate(valid_task_dict)
        result = run_task(task)

        assert result.status == TaskStatus.SUCCESS
        assert result.decision == "Buy"
        assert result.task_id == "test-001"
        assert result.error is None
        assert "market_report" in result.analysis_summary

    def test_config_maps_output_dir(self, valid_task_dict, mock_graph):
        task = TaskInput.model_validate(valid_task_dict)
        run_task(task)

        config = mock_graph.call_args[1]["config"]
        assert config["results_dir"] == task.output_dir

    def test_config_maps_llm_provider(self, valid_task_dict, mock_graph):
        valid_task_dict["llm_provider"] = "anthropic"
        valid_task_dict["deep_think_llm"] = "claude-3-opus"
        task = TaskInput.model_validate(valid_task_dict)
        run_task(task)

        config = mock_graph.call_args[1]["config"]
        assert config["llm_provider"] == "anthropic"
        assert config["deep_think_llm"] == "claude-3-opus"

    def test_graph_error_maps_to_internal(self, valid_task_dict):
        task = TaskInput.model_validate(valid_task_dict)
        with patch("extensions.run.runner.TradingAgentsGraph") as m:
            instance = MagicMock()
            instance.propagate.side_effect = RuntimeError("Something broke")
            m.return_value = instance

            with pytest.raises(InternalError) as exc:
                run_task(task)
            assert "Something broke" in str(exc.value)

    def test_graph_data_unavailable(self, valid_task_dict):
        task = TaskInput.model_validate(valid_task_dict)
        with patch("extensions.run.runner.TradingAgentsGraph") as m:
            instance = MagicMock()
            instance.propagate.side_effect = ValueError("No price data found for symbol XYZ")
            m.return_value = instance

            with pytest.raises(InternalError) as exc:
                run_task(task)
            assert "no data" in str(exc.value).lower() or "data" in str(exc.value).lower()


@pytest.mark.unit
class TestRunTaskFile:
    def test_missing_file(self):
        with pytest.raises(TaskValidationError, match="not found"):
            run_task_file("/nonexistent/task.json")

    def test_invalid_json(self, tmp_output):
        f = tmp_output / "bad.json"
        f.write_text("{invalid", encoding="utf-8")
        with pytest.raises(TaskValidationError, match="Invalid JSON"):
            run_task_file(str(f))

    def test_validation_error(self, tmp_output):
        f = tmp_output / "bad.json"
        f.write_text(json.dumps({"task_id": "", "symbol": ""}), encoding="utf-8")
        with pytest.raises(TaskValidationError, match="validation"):
            run_task_file(str(f))

    def test_writes_result_json(self, valid_task_file, mock_graph):
        result = run_task_file(str(valid_task_file))

        result_path = Path(result.artifacts["result.json"])
        assert result_path.exists()
        data = json.loads(result_path.read_text(encoding="utf-8"))
        assert data["status"] == "success"
        assert data["task_id"] == "test-001"

    def test_custom_result_path(self, valid_task_file, mock_graph, tmp_output):
        custom = tmp_output / "custom.json"
        result = run_task_file(str(valid_task_file), str(custom))

        assert Path(result.artifacts["result.json"]) == custom.resolve()
        assert custom.exists()
