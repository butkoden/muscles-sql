# Golden Tutorial (RU)

1. Установите пакет:
```bash
pip install -e ".[dev]"
```

2. Проверьте SQL слой:
```bash
muscles-sql doctor --url sqlite:///./app.db
```

3. Инициализируйте миграции:
```bash
muscles-sql migrate init --dir migrations
```

4. Сгенерируйте SQL-ресурс:
```bash
muscles-sql generate resource bookings --sql
```
