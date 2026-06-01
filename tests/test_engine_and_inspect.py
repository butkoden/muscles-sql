from muscles_sql.config import DatabaseConfig
from muscles_sql.engine import EngineManager
from muscles_sql.inspect import inspect_sql_layer


def test_engine_manager_and_inspect_sqlite():
    manager = EngineManager(DatabaseConfig(url="sqlite:///:memory:"))
    report = inspect_sql_layer(manager)
    assert report["status"] == "ok"
    assert report["dialect"] == "sqlite"
