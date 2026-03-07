class RollbarClientError(Exception):
    """Base exception for bc_rollbar_client."""


class RollbarInitError(RollbarClientError):
    """Raised when initialization fails (not initialized or already initialized)."""


class RollbarReportError(RollbarClientError):
    """Raised when reporting a message or exception to Rollbar fails."""
