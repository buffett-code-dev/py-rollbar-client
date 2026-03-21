import logging

from bc_rollbar_client.client import RollbarClient
from bc_rollbar_client.config import RollbarConfig
from bc_rollbar_client.exceptions import RollbarClientError, RollbarInitError, RollbarReportError
from bc_rollbar_client.level import RollbarLevel

__all__ = [
    "RollbarClient",
    "RollbarClientError",
    "RollbarConfig",
    "RollbarInitError",
    "RollbarLevel",
    "RollbarReportError",
    "get_instance",
    "init",
]

_client: RollbarClient | None = None


def init(
    config: RollbarConfig,
    logger: logging.Logger | None = None,
) -> None:
    global _client
    if _client is not None:
        raise RollbarInitError("RollbarClient is already initialized. init() must be called only once.")
    _client = RollbarClient(config=config, logger=logger)


def get_instance() -> RollbarClient:
    if _client is None:
        raise RollbarInitError("RollbarClient is not initialized. Call init() first.")
    return _client
