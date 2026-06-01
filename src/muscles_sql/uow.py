class UnitOfWork:
    def __init__(self, session_factory):
        self._session_factory = session_factory
        self.session = None

    def __enter__(self):
        self.session = self._session_factory()
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            self.session.commit()
        else:
            self.session.rollback()
        self.session.close()
