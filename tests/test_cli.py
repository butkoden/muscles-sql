import json
from pathlib import Path

from click.testing import CliRunner

from muscles_sql.cli import main


def test_doctor_and_inspect():
    runner = CliRunner()
    result = runner.invoke(main, ["doctor", "--url", "sqlite:///:memory:"])
    assert result.exit_code == 0
    assert json.loads(result.output)["status"] == "ok"

    result2 = runner.invoke(main, ["inspect", "--url", "sqlite:///:memory:"])
    assert result2.exit_code == 0
    assert json.loads(result2.output)["dialect"] == "sqlite"


def test_migrate_init_and_generate_sql(tmp_path):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=str(tmp_path)):
        res = runner.invoke(main, ["migrate", "init", "--dir", "migrations"])
        assert res.exit_code == 0
        gen = runner.invoke(main, ["generate", "resource", "booking", "--sql"])
        assert gen.exit_code == 0
        generated = Path("generated") / "booking.py"
        assert generated.exists()
        assert "sql_enabled = True" in generated.read_text(encoding="utf-8")


def test_migrate_v2_commands(monkeypatch):
    from muscles_sql import cli as cli_module

    calls = []

    monkeypatch.setattr("muscles_sql.migrations.revision", lambda **kwargs: calls.append(("revision", kwargs)))
    monkeypatch.setattr("muscles_sql.migrations.upgrade", lambda **kwargs: calls.append(("upgrade", kwargs)))
    monkeypatch.setattr("muscles_sql.migrations.downgrade", lambda **kwargs: calls.append(("downgrade", kwargs)))
    monkeypatch.setattr("muscles_sql.migrations.history", lambda **kwargs: calls.append(("history", kwargs)))
    monkeypatch.setattr("muscles_sql.migrations.current", lambda **kwargs: calls.append(("current", kwargs)))

    runner = CliRunner()
    url = "sqlite:///./app.db"
    assert runner.invoke(cli_module.main, ["migrate", "revision", "--message", "init", "--url", url]).exit_code == 0
    assert runner.invoke(cli_module.main, ["migrate", "upgrade", "--url", url]).exit_code == 0
    assert runner.invoke(cli_module.main, ["migrate", "downgrade", "--url", url]).exit_code == 0
    assert runner.invoke(cli_module.main, ["migrate", "history", "--url", url]).exit_code == 0
    assert runner.invoke(cli_module.main, ["migrate", "current", "--url", url]).exit_code == 0
    assert [name for name, _ in calls] == ["revision", "upgrade", "downgrade", "history", "current"]
    assert all(call_kwargs["url"] == url for _, call_kwargs in calls)
