# Muscles SQL

Muscles SQL is a data layer package for SQL databases:
- model-to-table mapping
- engine and session management
- repository CRUD and query API
- transactions and Unit of Work
- migrations (Alembic-compatible)
- inspect/doctor support

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
muscles-sql doctor --url sqlite:///./app.db
```
