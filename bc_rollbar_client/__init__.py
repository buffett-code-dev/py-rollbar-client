import logging

from bc_rollbar_client.client import RollbarClient
from bc_rollbar_client.exceptions import RollbarClientError, RollbarInitError, RollbarReportError
from bc_rollbar_client.level import RollbarLevel

__all__ = [
    "RollbarClient",
    "RollbarClientError",
    "RollbarInitError",
    "RollbarLevel",
    "RollbarReportError",
    "get_instance",
    "init",
]

_client: RollbarClient | None = None


def init(
    access_token: str,
    environment: str,
    logger: logging.Logger | None = None,
) -> None:
    global _client
    if _client is not None:
        raise RollbarInitError("RollbarClient is already initialized. init() must be called only once.")
    _client = RollbarClient(access_token=access_token, environment=environment, logger=logger)


def get_instance() -> RollbarClient:
    if _client is None:
        raise RollbarInitError("RollbarClient is not initialized. Call init() first.")
    return _client
