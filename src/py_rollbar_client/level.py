from enum import StrEnum


class RollbarLevel(StrEnum):
    """Rollbar log levels"""

    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"
