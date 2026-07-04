import subprocess
import sys
import os


def test_import_muscles_sql_does_not_eager_import_sqlalchemy():
    process = subprocess.run(
        [
            sys.executable,
            "-c",
            "import muscles_sql, sys; print('sqlalchemy' in sys.modules)",
        ],
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ, "PYTHONPATH": "src"},
    )
    assert process.returncode == 0
    assert process.stdout.strip() == "False"


def test_public_exports_are_importable():
    from muscles_sql import DatabaseConfig
    from muscles_sql import EngineManager
    from muscles_sql import FilterClause
    from muscles_sql import JoinClause
    from muscles_sql import QuerySpec
    from muscles_sql import SqlRepository
    from muscles_sql import UnitOfWork
    from muscles_sql import map_model

    assert DatabaseConfig.__name__ == "DatabaseConfig"
    assert EngineManager.__name__ == "EngineManager"
    assert FilterClause.__name__ == "FilterClause"
    assert JoinClause.__name__ == "JoinClause"
    assert QuerySpec.__name__ == "QuerySpec"
    assert SqlRepository.__name__ == "SqlRepository"
    assert UnitOfWork.__name__ == "UnitOfWork"
    assert callable(map_model)
