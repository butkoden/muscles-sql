from pathlib import Path


def init_migrations(target_dir: str = "migrations") -> Path:
    root = Path(target_dir)
    versions = root / "versions"
    root.mkdir(parents=True, exist_ok=True)
    versions.mkdir(parents=True, exist_ok=True)
    return root
