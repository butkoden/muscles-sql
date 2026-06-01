class UnitOfWork:
    def __init__(self, session_factory, *, isolation_level: str | None = None):
        self._session_factory = session_factory
        self._isolation_level = isolation_level
        self.session = None

    def __enter__(self):
        self.session = self._session_factory()
        if self._isolation_level:
            self.session.connection(execution_options={"isolation_level": self._isolation_level})
        return self

    def __exit__(self, exc_type, exc, tb):
        if exc_type is None:
            self.session.commit()
        else:
            self.session.rollback()
        self.session.close()

    def begin_nested(self):
        return self.session.begin_nested()

    def with_retry(self, fn, *, max_attempts: int = 3, retry_on: tuple[type[Exception], ...] = ()):
        if max_attempts < 1:
            raise ValueError("max_attempts must be >= 1")
        attempt = 0
        while True:
            attempt += 1
            try:
                return fn(self.session)
            except Exception as exc:
                if retry_on and isinstance(exc, retry_on) and attempt < max_attempts:
                    self.session.rollback()
                    continue
                raise
