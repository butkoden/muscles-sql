from muscles_sql.migrations import init_migrations
import pytest


def test_init_migrations(tmp_path):
    root = init_migrations(str(tmp_path / "migrations"))
    assert root.exists()
    assert (root / "versions").exists()
    assert (root / "env.py").exists()
    assert (root / "script.py.mako").exists()


def test_migration_commands_require_alembic(monkeypatch):
    import builtins
    from muscles_sql import migrations

    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name.startswith("alembic"):
            raise ModuleNotFoundError(name)
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", fake_import)
    with pytest.raises(RuntimeError):
        migrations.revision(message="init")
