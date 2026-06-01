from muscles_sql.mapping import map_model


class FakeColumn:
    def __init__(self, field_type, primary_key=False, nullable=True):
        self.field_type = field_type
        self.primary_key = primary_key
        self.nullable = nullable


class Integer:
    pass


class String:
    pass


class UserModel:
    id = FakeColumn(Integer, primary_key=True, nullable=False)
    name = FakeColumn(String, nullable=False)


def test_map_model_builds_table():
    table = map_model(UserModel, "users")
    assert table.name == "users"
    assert "id" in table.columns
    assert "name" in table.columns
    assert list(table.primary_key.columns)[0].name == "id"
    assert table.columns["id"].autoincrement is True
