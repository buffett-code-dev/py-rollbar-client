from bc_rollbar_client.client import RollbarClient
from bc_rollbar_client.level import RollbarLevel

__all__ = ["RollbarClient", "RollbarLevel", "init", "get_instance"]

_client: RollbarClient | None = None


def init(access_token: str, environment: str) -> None:
    global _client
    if _client is not None:
        raise RuntimeError("RollbarClient is already initialized. init() must be called only once.")
    _client = RollbarClient(access_token=access_token, environment=environment)


def get_instance() -> RollbarClient:
    if _client is None:
        raise RuntimeError("RollbarClient is not initialized. Call init() first.")
    return _client
