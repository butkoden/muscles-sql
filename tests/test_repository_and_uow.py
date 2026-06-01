from sqlalchemy import Column, Integer, MetaData, String, Table

from muscles_sql.config import DatabaseConfig
from muscles_sql.engine import EngineManager
from muscles_sql.repository import SqlRepository
from muscles_sql.uow import UnitOfWork


def _users_table():
    metadata = MetaData()
    return Table(
        "users",
        metadata,
        Column("id", Integer, primary_key=True),
        Column("name", String, nullable=False),
    ), metadata


def test_repository_crud_and_uow_commit():
    manager = EngineManager(DatabaseConfig(url="sqlite:///:memory:"))
    table, metadata = _users_table()
    metadata.create_all(manager.engine)

    with UnitOfWork(manager.session_factory) as uow:
        repo = SqlRepository(uow.session, table)
        pk = repo.create({"id": 1, "name": "Denis"})
        assert pk[0] == 1
        row = repo.get(1)
        assert row["name"] == "Denis"
        repo.update(1, {"name": "Butko"})
        row2 = repo.get(1)
        assert row2["name"] == "Butko"
        repo.delete(1)
        assert repo.get(1) is None


def test_repository_find_count_exists():
    manager = EngineManager(DatabaseConfig(url="sqlite:///:memory:"))
    table, metadata = _users_table()
    metadata.create_all(manager.engine)

    with UnitOfWork(manager.session_factory) as uow:
        repo = SqlRepository(uow.session, table)
        repo.create({"id": 1, "name": "Denis"})
        repo.create({"id": 2, "name": "Ira"})
        repo.create({"id": 3, "name": "Denis"})

        found = repo.find({"name": "Denis"})
        assert len(found) == 2
        assert repo.count({"name": "Denis"}) == 2
        assert repo.exists({"name": "Ira"}) is True
        assert repo.exists({"name": "Missing"}) is False
