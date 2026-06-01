import subprocess
import sys
import os


def test_import_muscles_sql_does_not_eager_import_sqlalchemy():
    process = subprocess.run(
        [
            sys.executable,
            "-c",
            "import muscles_sql, sys; print('sqlalchemy' in sys.modules)",
        ],
        capture_output=True,
        text=True,
        check=False,
        env={**os.environ, "PYTHONPATH": "src"},
    )
    assert process.returncode == 0
    assert process.stdout.strip() == "False"
