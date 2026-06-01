from typing import Any

from sqlalchemy import Boolean, Column, Date, DateTime, Float, Integer, MetaData, Numeric, String, Table, Text

metadata = MetaData()

TYPE_MAP: dict[str, Any] = {
    "String": String,
    "Text": Text,
    "Integer": Integer,
    "Numeric": Numeric,
    "Float": Float,
    "Boolean": Boolean,
    "Date": Date,
    "DateTime": DateTime,
}


def _resolve_type(column_type: Any):
    name = getattr(column_type, "__name__", str(column_type))
    return TYPE_MAP.get(name, String)


def map_model(model_cls: type, table_name: str | None = None) -> Table:
    columns = []
    for field_name, field_def in model_cls.__dict__.items():
        if field_name.startswith("_"):
            continue
        field_type = getattr(field_def, "field_type", None)
        if field_type is None:
            continue
        sql_type = _resolve_type(field_type)
        is_pk = bool(getattr(field_def, "primary_key", False))
        nullable = bool(getattr(field_def, "nullable", not is_pk))
        autoincrement = bool(
            getattr(field_def, "autoincrement", False)
            or (is_pk and sql_type is Integer)
        )
        columns.append(
            Column(
                field_name,
                sql_type,
                primary_key=is_pk,
                nullable=nullable,
                autoincrement=autoincrement,
            )
        )

    if not columns:
        raise ValueError(f"No mappable columns found in model {model_cls.__name__}")
    return Table(table_name or model_cls.__name__.lower(), metadata, *columns, extend_existing=True)
