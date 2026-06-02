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
    monkeypatch.setenv("MUSCLES_SQL_URL", "sqlite:///./app.db")
    with pytest.raises(RuntimeError):
        migrations.revision(message="init")


def test_config_uses_env_url_and_target_metadata(monkeypatch):
    from muscles_sql import migrations

    class FakeConfig:
        def __init__(self):
            self.main_options = {}
            self.attributes = {}

        def set_main_option(self, key, value):
            self.main_options[key] = value

    monkeypatch.setenv("MUSCLES_SQL_URL", "sqlite:///./app.db")
    monkeypatch.setattr(migrations, "_load_alembic", lambda: (object(), FakeConfig))

    cfg = migrations._config(target_dir="migrations", target_metadata={"tables": []})

    assert cfg.main_options["script_location"] == "migrations"
    assert cfg.main_options["sqlalchemy.url"] == "sqlite:///./app.db"
    assert cfg.attributes["target_metadata"] == {"tables": []}
