# Muscles SQL Architecture

Muscles SQL is a dedicated SQL data layer:
- `config.py`: database config
- `engine.py`: engine/session factory and pooling
- `mapping.py`: Muscles Model/Column to SQL table mapping
- `repository.py`: CRUD/query API
- `uow.py`: Unit of Work and transactions
- `migrations.py`: Alembic-compatible bootstrap
- `inspect.py`: inspect/doctor contract
- `cli.py`: AI-first commands (`doctor`, `inspect`, `migrate`, `generate --sql`)
- compatible with core DI optimization (`muscles#36`): sql CLI/runtime path has no behavior regression.
