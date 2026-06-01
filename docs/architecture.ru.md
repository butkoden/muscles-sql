# Архитектура Muscles SQL

Muscles SQL строится как отдельный слой данных:
- `config.py` — конфигурация БД
- `engine.py` — engine/session factory
- `mapping.py` — преобразование Muscles Model/Column в SQL table
- `repository.py` — CRUD/query API
- `uow.py` — Unit of Work
- `migrations.py` — Alembic-compatible bootstrap
- `inspect.py` — контракт диагностики для `inspect`/`doctor`
- `cli.py` — AI-first CLI (`doctor`, `inspect`, `migrate`, `generate --sql`)
- совместим с оптимизацией DI из core (`muscles#36`): без регрессий поведения SQL CLI/runtime path.
