from __future__ import annotations

from typing import Any


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

        stmt = select(self.table)
        filters = filters or {}
        for field, value in filters.items():
            stmt = stmt.where(getattr(self.table.c, field) == value)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        stmt = stmt.limit(limit).offset(offset)
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
