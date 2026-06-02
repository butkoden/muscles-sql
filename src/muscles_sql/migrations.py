from pathlib import Path
import os
from typing import Any


def init_migrations(target_dir: str = "migrations") -> Path:
    root = Path(target_dir)
    versions = root / "versions"
    root.mkdir(parents=True, exist_ok=True)
    versions.mkdir(parents=True, exist_ok=True)
    _ensure_bootstrap_files(root)
    return root


def _ensure_bootstrap_files(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    env_py = root / "env.py"
    script_mako = root / "script.py.mako"
    readme = root / "README"
    if not env_py.exists():
        env_py.write_text(
            "from __future__ import annotations\n"
            "from alembic import context\n"
            "from sqlalchemy import engine_from_config, pool\n\n"
            "config = context.config\n"
            "target_metadata = config.attributes.get('target_metadata')\n\n"
            "def run_migrations_offline():\n"
            "    url = config.get_main_option('sqlalchemy.url')\n"
            "    context.configure(url=url, target_metadata=target_metadata, literal_binds=True)\n"
            "    with context.begin_transaction():\n"
            "        context.run_migrations()\n\n"
            "def run_migrations_online():\n"
            "    connectable = engine_from_config(config.get_section(config.config_ini_section) or {}, prefix='sqlalchemy.', poolclass=pool.NullPool)\n"
            "    with connectable.connect() as connection:\n"
            "        context.configure(connection=connection, target_metadata=target_metadata)\n"
            "        with context.begin_transaction():\n"
            "            context.run_migrations()\n\n"
            "if context.is_offline_mode():\n"
            "    run_migrations_offline()\n"
            "else:\n"
            "    run_migrations_online()\n",
            encoding="utf-8",
        )
    if not script_mako.exists():
        script_mako.write_text(
            "\"\"\"${message}\n\n"
            "Revision ID: ${up_revision}\n"
            "Revises: ${down_revision | comma,n}\n"
            "Create Date: ${create_date}\n"
            "\"\"\"\n\n"
            "from alembic import op\n"
            "import sqlalchemy as sa\n\n"
            "revision = ${repr(up_revision)}\n"
            "down_revision = ${repr(down_revision)}\n"
            "branch_labels = ${repr(branch_labels)}\n"
            "depends_on = ${repr(depends_on)}\n\n"
            "def upgrade():\n"
            "    pass\n\n"
            "def downgrade():\n"
            "    pass\n",
            encoding="utf-8",
        )
    if not readme.exists():
        readme.write_text("Muscles SQL Alembic migration environment.\n", encoding="utf-8")


def _load_alembic():
    try:
        from alembic import command
        from alembic.config import Config
    except Exception as exc:
        raise RuntimeError("Alembic is required for migration commands") from exc
    return command, Config


def _resolve_url(url: str | None = None) -> str | None:
    if url:
        return url
    env_url = os.getenv("MUSCLES_SQL_URL")
    if env_url:
        return env_url
    return None


def _config(target_dir: str = "migrations", url: str | None = None, target_metadata: Any | None = None):
    _, Config = _load_alembic()
    root = Path(target_dir)
    _ensure_bootstrap_files(root)
    cfg = Config()
    cfg.set_main_option("script_location", target_dir)
    resolved_url = _resolve_url(url)
    if not resolved_url:
        raise ValueError("Database URL is required for migration commands")
    cfg.set_main_option("sqlalchemy.url", resolved_url)
    if target_metadata is not None:
        cfg.attributes["target_metadata"] = target_metadata
    return cfg


def revision(
    message: str,
    target_dir: str = "migrations",
    autogenerate: bool = False,
    url: str | None = None,
    target_metadata: Any | None = None,
) -> None:
    command, _ = _load_alembic()
    command.revision(
        _config(target_dir, url=url, target_metadata=target_metadata),
        message=message,
        autogenerate=autogenerate,
    )


def upgrade(rev: str = "head", target_dir: str = "migrations", url: str | None = None) -> None:
    command, _ = _load_alembic()
    command.upgrade(_config(target_dir, url=url), rev)


def downgrade(rev: str = "-1", target_dir: str = "migrations", url: str | None = None) -> None:
    command, _ = _load_alembic()
    command.downgrade(_config(target_dir, url=url), rev)


def history(target_dir: str = "migrations", url: str | None = None) -> None:
    command, _ = _load_alembic()
    command.history(_config(target_dir, url=url))


def current(target_dir: str = "migrations", url: str | None = None) -> None:
    command, _ = _load_alembic()
    command.current(_config(target_dir, url=url))
