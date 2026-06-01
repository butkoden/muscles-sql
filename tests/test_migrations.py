from muscles_sql.migrations import init_migrations


def test_init_migrations(tmp_path):
    root = init_migrations(str(tmp_path / "migrations"))
    assert root.exists()
    assert (root / "versions").exists()
