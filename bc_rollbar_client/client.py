import logging
from typing import Any

import rollbar

from bc_rollbar_client.config import RollbarConfig
from bc_rollbar_client.exceptions import RollbarReportError
from bc_rollbar_client.level import RollbarLevel

_default_logger = logging.getLogger(__name__)


class RollbarClient:
    """
    A lightweight wrapper for the Rollbar SDK.

    Handles initialization and provides synchronous error reporting
    (waits for each report to be sent before returning).

    Do not instantiate this class directly. Use bc_rollbar_client.init() /
    bc_rollbar_client.get_instance() instead.
    """

    def __init__(
        self,
        config: RollbarConfig,
        logger: logging.Logger | None = None,
    ) -> None:
        self._logger = logger or _default_logger
        rollbar.init(access_token=config.access_token, environment=config.environment)
        self._logger.info(f"Rollbar initialized (environment: {config.environment})")

    def report_message(
        self,
        message: str,
        level: RollbarLevel = RollbarLevel.ERROR,
        extra_data: dict[str, Any] | None = None,
    ) -> None:
        """Send a message to Rollbar."""
        try:
            rollbar.report_message(message, level.value, extra_data=extra_data)
            rollbar.wait()
        except Exception as e:
            raise RollbarReportError(f"Failed to report message: {e}") from e
        self._logger.info(f"Report message: {message}, level: {level.value}")

    def report_exception(
        self,
        level: RollbarLevel = RollbarLevel.ERROR,
        extra_data: dict[str, Any] | None = None,
    ) -> None:
        """Send the current exception to Rollbar. Must be called within an except block."""
        try:
            rollbar.report_exc_info(level=level.value, extra_data=extra_data)
            rollbar.wait()
        except Exception as e:
            raise RollbarReportError(f"Failed to report exception: {e}") from e
        self._logger.info(f"Report exception: {level.value}, extra_data: {extra_data}")
