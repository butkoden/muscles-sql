from __future__ import annotations

__all__ = [
    "DatabaseConfig",
    "EngineManager",
    "map_model",
    "SqlRepository",
    "UnitOfWork",
    "QuerySpec",
    "FilterClause",
    "JoinClause",
    "SqlResourceGeneratorProvider",
]


def __getattr__(name: str):
    if name == "DatabaseConfig":
        from .config import DatabaseConfig

        return DatabaseConfig
    if name == "EngineManager":
        from .engine import EngineManager

        return EngineManager
    if name == "map_model":
        from .mapping import map_model

        return map_model
    if name == "SqlRepository":
        from .repository import SqlRepository

        return SqlRepository
    if name == "UnitOfWork":
        from .uow import UnitOfWork

        return UnitOfWork
    if name == "QuerySpec":
        from .query import QuerySpec

        return QuerySpec
    if name == "FilterClause":
        from .query import FilterClause

        return FilterClause
    if name == "JoinClause":
        from .query import JoinClause

        return JoinClause
    if name == "SqlResourceGeneratorProvider":
        from .providers import SqlResourceGeneratorProvider

        return SqlResourceGeneratorProvider
    raise AttributeError(name)
