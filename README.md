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
