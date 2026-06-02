from __future__ import annotations

from typing import Any

from .query import FilterClause, JoinClause, QuerySpec


class SqlRepository:
    def __init__(self, session, table):
        self.session = session
        self.table = table

    def create(self, data: dict):
        from sqlalchemy import insert

        result = self.session.execute(insert(self.table).values(**data))
        return result.inserted_primary_key

    def get(self, pk):
        from sqlalchemy import select

        pk_col = list(self.table.primary_key.columns)[0]
        stmt = select(self.table).where(pk_col == pk)
        return self.session.execute(stmt).mappings().first()

    def list(self, limit: int = 100, offset: int = 0, order_by: Any = None):
        from sqlalchemy import select

        stmt = select(self.table).limit(limit).offset(offset)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        return self.session.execute(stmt).mappings().all()

    def find(self, filters: dict | None = None, limit: int = 100, offset: int = 0, order_by: Any = None):
        from sqlalchemy import select

        clauses = [FilterClause(field=field, op="eq", value=value) for field, value in (filters or {}).items()]
        spec = QuerySpec(filters=clauses, limit=limit, offset=offset, order_by=[order_by] if order_by is not None else [])
        stmt = self._build_select(spec)
        return self.session.execute(stmt).mappings().all()

    def count(self, filters: dict | None = None) -> int:
        from sqlalchemy import func, select

        stmt = select(func.count()).select_from(self.table)
        filters = filters or {}
        for field, value in filters.items():
            stmt = stmt.where(getattr(self.table.c, field) == value)
        return int(self.session.execute(stmt).scalar_one())

    def exists(self, filters: dict) -> bool:
        return self.count(filters) > 0

    def update(self, pk, data: dict):
        from sqlalchemy import update

        pk_col = list(self.table.primary_key.columns)[0]
        stmt = update(self.table).where(pk_col == pk).values(**data)
        return self.session.execute(stmt).rowcount

    def delete(self, pk):
        from sqlalchemy import delete

        pk_col = list(self.table.primary_key.columns)[0]
        stmt = delete(self.table).where(pk_col == pk)
        return self.session.execute(stmt).rowcount

    def query(self, spec: QuerySpec):
        stmt = self._build_select(spec)
        return self.session.execute(stmt).mappings().all()

    def first(self, spec: QuerySpec):
        first_spec = QuerySpec(
            filters=list(spec.filters),
            or_filters=list(spec.or_filters),
            joins=list(spec.joins),
            select_columns=list(spec.select_columns),
            order_by=list(spec.order_by),
            group_by=list(spec.group_by),
            having=list(spec.having),
            limit=1,
            offset=spec.offset,
            distinct=spec.distinct,
        )
        stmt = self._build_select(first_spec)
        return self.session.execute(stmt).mappings().first()

    def scalar(self, spec: QuerySpec):
        stmt = self._build_select(spec)
        return self.session.execute(stmt).scalar()

    def aggregate(self, spec: QuerySpec):
        stmt = self._build_select(spec)
        return self.session.execute(stmt).mappings().all()

    def bulk_create(self, rows: list[dict]) -> int:
        from sqlalchemy import insert

        if not rows:
            return 0
        self.session.execute(insert(self.table), rows)
        return len(rows)

    def bulk_update(self, pk_field: str, rows: list[dict]) -> int:
        if not rows:
            return 0
        updated = 0
        for row in rows:
            pk = row.get(pk_field)
            if pk is None:
                continue
            data = {k: v for k, v in row.items() if k != pk_field}
            if not data:
                continue
            updated += int(self.update(pk, data) or 0)
        return updated

    def upsert(self, row: dict, conflict_fields: list[str]):
        from sqlalchemy import inspect
        from sqlalchemy.dialects.sqlite import insert as sqlite_insert
        from sqlalchemy.exc import OperationalError

        if not self._has_unique_conflict_constraint(conflict_fields):
            raise ValueError(
                "conflict_fields must match a PRIMARY KEY or UNIQUE constraint for safe upsert fallback"
            )

        dialect_name = inspect(self.session.bind).dialect.name
        if dialect_name == "sqlite":
            stmt = sqlite_insert(self.table).values(**row)
            update_data = {k: v for k, v in row.items() if k not in conflict_fields}
            stmt = stmt.on_conflict_do_update(index_elements=conflict_fields, set_=update_data)
            try:
                self.session.execute(stmt)
                return 1
            except OperationalError:
                # Fallback for tables where conflict_fields are not backed by unique/pk constraints.
                pass

        filters = {field: row[field] for field in conflict_fields if field in row}
        if filters:
            existing = self.find(filters=filters, limit=1)
            if existing:
                pk_col = list(self.table.primary_key.columns)[0].name
                pk_val = existing[0][pk_col]
                return self.update(pk_val, {k: v for k, v in row.items() if k != pk_col})

        pk_col = list(self.table.primary_key.columns)[0].name
        pk_val = row.get(pk_col)
        if pk_val is not None and self.get(pk_val):
            return self.update(pk_val, {k: v for k, v in row.items() if k != pk_col})
        self.create(row)
        return 1

    def _has_unique_conflict_constraint(self, conflict_fields: list[str]) -> bool:
        if not conflict_fields:
            return False
        conflict_set = set(conflict_fields)
        pk_cols = {column.name for column in self.table.primary_key.columns}
        if conflict_set == pk_cols:
            return True

        for constraint in getattr(self.table, "constraints", []):
            columns = getattr(constraint, "columns", None)
            if columns is None:
                continue
            if getattr(constraint, "unique", False) and {column.name for column in columns} == conflict_set:
                return True

        for index in getattr(self.table, "indexes", []):
            if getattr(index, "unique", False) and {column.name for column in index.columns} == conflict_set:
                return True

        return False

    def _build_select(self, spec: QuerySpec):
        from sqlalchemy import and_, or_, select

        columns = spec.select_columns or [self.table]
        stmt = select(*columns)
        if spec.distinct:
            stmt = stmt.distinct()

        for join in spec.joins:
            if join.is_outer:
                stmt = stmt.outerjoin(join.table, join.on)
            else:
                stmt = stmt.join(join.table, join.on)

        if spec.filters:
            stmt = stmt.where(and_(*[self._build_filter_expr(clause) for clause in spec.filters]))
        if spec.or_filters:
            stmt = stmt.where(or_(*[self._build_filter_expr(clause) for clause in spec.or_filters]))
        if spec.group_by:
            stmt = stmt.group_by(*spec.group_by)
        if spec.having:
            stmt = stmt.having(*spec.having)
        if spec.order_by:
            stmt = stmt.order_by(*spec.order_by)
        if spec.limit is not None:
            stmt = stmt.limit(spec.limit)
        if spec.offset:
            stmt = stmt.offset(spec.offset)
        return stmt

    def _build_filter_expr(self, clause: FilterClause):
        column = getattr(self.table.c, clause.field)
        op = clause.op.lower()
        if op == "eq":
            return column == clause.value
        if op == "ne":
            return column != clause.value
        if op == "gt":
            return column > clause.value
        if op == "gte":
            return column >= clause.value
        if op == "lt":
            return column < clause.value
        if op == "lte":
            return column <= clause.value
        if op == "in":
            return column.in_(clause.value or [])
        if op == "like":
            return column.like(clause.value)
        if op == "is_null":
            return column.is_(None) if clause.value else column.is_not(None)
        raise ValueError(f"Unsupported filter operator: {clause.op}")
