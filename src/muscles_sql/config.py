from dataclasses import dataclass


@dataclass(slots=True)
class DatabaseConfig:
    url: str
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10
    future: bool = True
