from dataclasses import dataclass


@dataclass(frozen=True)
class RollbarConfig:
    access_token: str
    environment: str

    def __post_init__(self) -> None:
        if not self.access_token:
            raise ValueError("access_token must not be empty")
        if not self.environment:
            raise ValueError("environment must not be empty")
