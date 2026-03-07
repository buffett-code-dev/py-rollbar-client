import logging
from typing import Any

import rollbar

from bc_rollbar_client.level import RollbarLevel

logger = logging.getLogger(__name__)


class RollbarClient:
    """
    A lightweight wrapper for the Rollbar SDK.

    Handles initialization and provides synchronous error reporting
    (waits for each report to be sent before returning).

    Do not instantiate this class directly. Use bc_rollbar_client.init() /
    bc_rollbar_client.get_instance() instead.
    """

    def __init__(self, access_token: str, environment: str) -> None:
        rollbar.init(access_token=access_token, environment=environment)
        logger.info(f"Rollbar initialized (environment: {environment})")

    def report_message(
        self,
        message: str,
        level: RollbarLevel = RollbarLevel.ERROR,
        extra_data: dict[str, Any] | None = None,
    ) -> None:
        """Send a message to Rollbar."""
        rollbar.report_message(message, level.value, extra_data=extra_data)
        rollbar.wait()
        logger.info(f"Report message: {message}, level: {level.value}")

    def report_exception(
        self,
        level: RollbarLevel = RollbarLevel.ERROR,
        extra_data: dict[str, Any] | None = None,
    ) -> None:
        """Send the current exception to Rollbar. Must be called within an except block."""
        rollbar.report_exc_info(level=level.value, extra_data=extra_data)
        rollbar.wait()
        logger.info(f"Report exception: {level.value}, extra_data: {extra_data}")
