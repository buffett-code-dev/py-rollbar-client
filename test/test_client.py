from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

import bc_rollbar_client
from bc_rollbar_client import RollbarClient, RollbarConfig, RollbarLevel
from bc_rollbar_client.exceptions import RollbarInitError, RollbarReportError


@pytest.fixture(autouse=True)
def _reset_client() -> Generator[None]:
    bc_rollbar_client._client = None
    yield
    bc_rollbar_client._client = None


@pytest.fixture()
def mock_rollbar() -> Generator[MagicMock]:
    with patch("bc_rollbar_client.client.rollbar") as mock:
        yield mock


class TestRollbarClient:
    def test_init(self, mock_rollbar: MagicMock) -> None:
        RollbarClient(config=RollbarConfig(access_token="test_token", environment="production"))
        mock_rollbar.init.assert_called_once_with(access_token="test_token", environment="production")

    def test_report_message(self, mock_rollbar: MagicMock) -> None:
        client = RollbarClient(config=RollbarConfig(access_token="test_token", environment="production"))
        client.report_message("test message", level=RollbarLevel.WARNING)

        mock_rollbar.report_message.assert_called_once_with("test message", "warning", extra_data=None)
        mock_rollbar.wait.assert_called()

    def test_report_message_with_extra_data(self, mock_rollbar: MagicMock) -> None:
        client = RollbarClient(config=RollbarConfig(access_token="test_token", environment="production"))
        extra = {"key": "value"}
        client.report_message("test", extra_data=extra)

        mock_rollbar.report_message.assert_called_once_with("test", "error", extra_data=extra)

    def test_report_exception(self, mock_rollbar: MagicMock) -> None:
        client = RollbarClient(config=RollbarConfig(access_token="test_token", environment="production"))
        client.report_exception(level=RollbarLevel.ERROR)

        mock_rollbar.report_exc_info.assert_called_once_with(level="error", extra_data=None)
        mock_rollbar.wait.assert_called()

    def test_report_exception_with_extra_data(self, mock_rollbar: MagicMock) -> None:
        client = RollbarClient(config=RollbarConfig(access_token="test_token", environment="production"))
        extra = {"request_id": "abc123"}
        client.report_exception(level=RollbarLevel.WARNING, extra_data=extra)

        mock_rollbar.report_exc_info.assert_called_once_with(level="warning", extra_data=extra)


class TestModuleAccessor:
    def test_init_and_get_instance(self, mock_rollbar: MagicMock) -> None:
        bc_rollbar_client.init(config=RollbarConfig(access_token="token", environment="staging"))
        client = bc_rollbar_client.get_instance()
        assert isinstance(client, RollbarClient)
        mock_rollbar.init.assert_called_once_with(access_token="token", environment="staging")

    def test_get_instance_before_init_raises(self) -> None:
        with pytest.raises(RollbarInitError, match="not initialized"):
            bc_rollbar_client.get_instance()

    def test_init_twice_raises(self, mock_rollbar: MagicMock) -> None:
        bc_rollbar_client.init(config=RollbarConfig(access_token="token", environment="staging"))
        with pytest.raises(RollbarInitError, match="already initialized"):
            bc_rollbar_client.init(config=RollbarConfig(access_token="token2", environment="production"))


class TestRollbarConfig:
    def test_empty_access_token_raises(self) -> None:
        with pytest.raises(ValueError, match="access_token must not be empty"):
            RollbarConfig(access_token="", environment="production")

    def test_empty_environment_raises(self) -> None:
        with pytest.raises(ValueError, match="environment must not be empty"):
            RollbarConfig(access_token="token", environment="")


class TestReportError:
    def test_report_message_failure(self, mock_rollbar: MagicMock) -> None:
        mock_rollbar.report_message.side_effect = Exception("connection error")
        client = RollbarClient(config=RollbarConfig(access_token="test_token", environment="production"))

        with pytest.raises(RollbarReportError, match="Failed to report message"):
            client.report_message("test")

    def test_report_exception_failure(self, mock_rollbar: MagicMock) -> None:
        mock_rollbar.report_exc_info.side_effect = Exception("connection error")
        client = RollbarClient(config=RollbarConfig(access_token="test_token", environment="production"))

        with pytest.raises(RollbarReportError, match="Failed to report exception"):
            client.report_exception()
