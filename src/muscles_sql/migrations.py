from pathlib import Path


def init_migrations(target_dir: str = "migrations") -> Path:
    root = Path(target_dir)
    versions = root / "versions"
    root.mkdir(parents=True, exist_ok=True)
    versions.mkdir(parents=True, exist_ok=True)
    return root


def _load_alembic():
    try:
        from alembic import command
        from alembic.config import Config
    except Exception as exc:
        raise RuntimeError("Alembic is required for migration commands") from exc
    return command, Config


def _config(target_dir: str = "migrations"):
    _, Config = _load_alembic()
    cfg = Config()
    cfg.set_main_option("script_location", target_dir)
    return cfg


def revision(message: str, target_dir: str = "migrations", autogenerate: bool = False) -> None:
    command, _ = _load_alembic()
    command.revision(_config(target_dir), message=message, autogenerate=autogenerate)


def upgrade(rev: str = "head", target_dir: str = "migrations") -> None:
    command, _ = _load_alembic()
    command.upgrade(_config(target_dir), rev)


def downgrade(rev: str = "-1", target_dir: str = "migrations") -> None:
    command, _ = _load_alembic()
    command.downgrade(_config(target_dir), rev)


def history(target_dir: str = "migrations") -> None:
    command, _ = _load_alembic()
    command.history(_config(target_dir))


def current(target_dir: str = "migrations") -> None:
    command, _ = _load_alembic()
    command.current(_config(target_dir))
