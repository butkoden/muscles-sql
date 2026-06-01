# Golden Tutorial (EN)

1. Install package:
```bash
pip install -e ".[dev]"
```

2. Validate SQL layer:
```bash
muscles-sql doctor --url sqlite:///./app.db
```

3. Initialize migrations:
```bash
muscles-sql migrate init --dir migrations
```

4. Generate SQL resource:
```bash
muscles-sql generate resource bookings --sql
```
