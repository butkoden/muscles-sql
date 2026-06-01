import json

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
