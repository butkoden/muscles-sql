# Архитектура Muscles SQL

Muscles SQL строится как отдельный слой данных:
- `config.py` — конфигурация БД
- `engine.py` — engine/session factory
- `mapping.py` — преобразование Muscles Model/Column в SQL table
- `query.py` — декларативный контракт запросов (`QuerySpec`, filters, joins)
- `repository.py` — CRUD + advanced query/aggregate/upsert/bulk API
- `uow.py` — Unit of Work, nested transaction, retry helpers
- `migrations.py` — Alembic-compatible bootstrap + migration-команды v2
- `inspect.py` — контракт диагностики `inspect`/`doctor` с latency/schema отчётом
- `cli.py` — AI-first CLI (`doctor`, `inspect`, `migrate`, `generate --sql`)
- совместим с оптимизацией DI из core (`muscles#36`): без регрессий поведения SQL CLI/runtime path.
