from sqlalchemy import delete, insert, select, update


class SqlRepository:
    def __init__(self, session, table):
        self.session = session
        self.table = table

    def create(self, data: dict):
        result = self.session.execute(insert(self.table).values(**data))
        return result.inserted_primary_key

    def get(self, pk):
        pk_col = list(self.table.primary_key.columns)[0]
        stmt = select(self.table).where(pk_col == pk)
        return self.session.execute(stmt).mappings().first()

    def list(self, limit: int = 100, offset: int = 0):
        stmt = select(self.table).limit(limit).offset(offset)
        return self.session.execute(stmt).mappings().all()

    def update(self, pk, data: dict):
        pk_col = list(self.table.primary_key.columns)[0]
        stmt = update(self.table).where(pk_col == pk).values(**data)
        return self.session.execute(stmt).rowcount

    def delete(self, pk):
        pk_col = list(self.table.primary_key.columns)[0]
        stmt = delete(self.table).where(pk_col == pk)
        return self.session.execute(stmt).rowcount
