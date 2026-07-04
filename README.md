# Muscles SQL

Muscles SQL is a data layer package for SQL databases:
- model-to-table mapping
- engine and session management
- repository CRUD and advanced query API (filters/operators/joins/aggregates)
- transactions and Unit of Work (nested/savepoint/retry helpers)
- migrations v2 commands (Alembic-compatible lazy-load)
- inspect/doctor support with machine-readable diagnostics

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
muscles-sql doctor --url sqlite:///./app.db
```

## Named SQL Connections

`muscles-sql` can manage multiple SQL connections without becoming a generic
storage registry. The registry is SQL-only: it owns SQL connection configs,
lazy SQLAlchemy `EngineManager` instances, sessions, inspect and doctor reports.

```python
from muscles_sql import SqlConnectionConfig, SqlConnectionRegistry

registry = SqlConnectionRegistry(
    [
        SqlConnectionConfig(name="default", url="sqlite:///./app.db"),
        SqlConnectionConfig(name="analytics", url="sqlite:///./analytics.db", role="read"),
    ]
)

session = registry.session("analytics")
report = registry.inspect("analytics")
```

CLI diagnostics can read a JSON config:

```json
{
  "connections": {
    "default": "sqlite:///./app.db",
    "analytics": {"url": "sqlite:///./analytics.db", "role": "read"}
  }
}
```

```bash
muscles-sql inspect --config sql-connections.json --connection analytics
muscles-sql doctor --config sql-connections.json --all
```

Diagnostic output uses safe URLs and does not print passwords from DSNs.

## Advanced Query Example

```python
from sqlalchemy import func
from muscles_sql import FilterClause, JoinClause, QuerySpec, SqlRepository

spec = QuerySpec(
    filters=[FilterClause("status", "eq", "active")],
    joins=[JoinClause(table=orders, on=users.c.id == orders.c.user_id)],
    select_columns=[users.c.id, func.count(orders.c.id).label("orders_total")],
    group_by=[users.c.id],
    order_by=[users.c.id.asc()],
)
rows = SqlRepository(session, users).aggregate(spec)
```
