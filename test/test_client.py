from unittest.mock import MagicMock, patch

import pytest

from py_rollbar_client import RollbarClient, RollbarLevel


class TestRollbarClient:
    @patch("py_rollbar_client.client.rollbar")
    def test_init(self, mock_rollbar: MagicMock) -> None:
        RollbarClient(access_token="test_token", environment="production")
        mock_rollbar.init.assert_called_once_with(
            access_token="test_token", environment="production"
        )

    @patch("py_rollbar_client.client.rollbar")
    def test_report_message(self, mock_rollbar: MagicMock) -> None:
        client = RollbarClient(access_token="test_token", environment="production")
        client.report_message("test message", level=RollbarLevel.WARNING)

        mock_rollbar.report_message.assert_called_once_with(
            "test message", "warning", extra_data=None
        )
        mock_rollbar.wait.assert_called()

    @patch("py_rollbar_client.client.rollbar")
    def test_report_message_with_extra_data(self, mock_rollbar: MagicMock) -> None:
        client = RollbarClient(access_token="test_token", environment="production")
        extra = {"key": "value"}
        client.report_message("test", extra_data=extra)

        mock_rollbar.report_message.assert_called_once_with(
            "test", "error", extra_data=extra
        )

    @patch("py_rollbar_client.client.rollbar")
    def test_report_exception(self, mock_rollbar: MagicMock) -> None:
        client = RollbarClient(access_token="test_token", environment="production")
        client.report_exception(level=RollbarLevel.ERROR)

        mock_rollbar.report_exc_info.assert_called_once_with(
            level="error", extra_data=None
        )
        mock_rollbar.wait.assert_called()

    @patch("py_rollbar_client.client.rollbar")
    def test_report_exception_with_extra_data(self, mock_rollbar: MagicMock) -> None:
        client = RollbarClient(access_token="test_token", environment="production")
        extra = {"request_id": "abc123"}
        client.report_exception(level=RollbarLevel.WARNING, extra_data=extra)

        mock_rollbar.report_exc_info.assert_called_once_with(
            level="warning", extra_data=extra
        )
