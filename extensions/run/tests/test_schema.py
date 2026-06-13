import pytest

from extensions.run.schema import TaskInput, TaskStatus, ResultOutput, build_result


@pytest.mark.unit
class TestTaskInputValidation:
    def test_valid_minimal(self, valid_task_dict):
        task = TaskInput.model_validate(valid_task_dict)
        assert task.symbol == "AAPL"
        assert task.task_id == "test-001"
        assert task.analysis_date == "2024-05-10"

    def test_symbol_uppercased(self, valid_task_dict):
        valid_task_dict["symbol"] = "aapl"
        task = TaskInput.model_validate(valid_task_dict)
        assert task.symbol == "AAPL"

    def test_empty_symbol(self, valid_task_dict):
        valid_task_dict["symbol"] = ""
        with pytest.raises(ValueError, match="symbol must not be empty"):
            TaskInput.model_validate(valid_task_dict)

    def test_empty_task_id(self, valid_task_dict):
        valid_task_dict["task_id"] = "   "
        with pytest.raises(ValueError, match="task_id must not be empty"):
            TaskInput.model_validate(valid_task_dict)

    def test_invalid_schema_version(self, valid_task_dict):
        valid_task_dict["schema_version"] = "2.0"
        with pytest.raises(ValueError, match="Unsupported schema_version"):
            TaskInput.model_validate(valid_task_dict)

    def test_invalid_date_format(self, valid_task_dict):
        valid_task_dict["analysis_date"] = "2024/05/10"
        with pytest.raises(ValueError, match="YYYY-MM-DD"):
            TaskInput.model_validate(valid_task_dict)

    def test_invalid_date_value(self, valid_task_dict):
        valid_task_dict["analysis_date"] = "2024-13-01"
        with pytest.raises(ValueError, match="Invalid date"):
            TaskInput.model_validate(valid_task_dict)

    def test_default_analysts(self, valid_task_dict):
        task = TaskInput.model_validate(valid_task_dict)
        assert task.analysts == ["market", "social", "news", "fundamentals"]

    def test_custom_analysts(self, valid_task_dict):
        valid_task_dict["analysts"] = ["market", "news"]
        task = TaskInput.model_validate(valid_task_dict)
        assert task.analysts == ["market", "news"]

    def test_research_depth_clamped(self, valid_task_dict):
        valid_task_dict["research_depth"] = 0
        task = TaskInput.model_validate(valid_task_dict)
        assert task.research_depth == 1

        valid_task_dict["research_depth"] = 99
        task = TaskInput.model_validate(valid_task_dict)
        assert task.research_depth == 10

    def test_defaults(self, valid_task_dict):
        task = TaskInput.model_validate(valid_task_dict)
        assert task.asset_type == "stock"
        assert task.llm_provider is None
        assert task.output_language == "English"
        assert task.checkpoint_enabled is False


@pytest.mark.unit
class TestResultOutput:
    def test_build_success(self, valid_task_dict):
        task = TaskInput.model_validate(valid_task_dict)
        result = build_result(
            task=task,
            status=TaskStatus.SUCCESS,
            decision="Buy",
            final_state={"market_report": "Strong buy"},
        )
        assert result.status == TaskStatus.SUCCESS
        assert result.decision == "Buy"
        assert result.analysis_summary["market_report"] == "Strong buy"
        assert result.task_id == "test-001"
        assert result.error is None

    def test_build_error(self, valid_task_dict):
        from extensions.run.schema import ErrorInfo
        task = TaskInput.model_validate(valid_task_dict)
        result = build_result(
            task=task,
            status=TaskStatus.DATA_UNAVAILABLE,
            error=ErrorInfo(code="data_unavailable", message="No price data"),
        )
        assert result.status == TaskStatus.DATA_UNAVAILABLE
        assert result.error is not None
        assert result.error.code == "data_unavailable"
        assert result.decision is None
