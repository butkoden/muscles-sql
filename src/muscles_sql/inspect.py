from sqlalchemy import text


def inspect_sql_layer(engine_manager) -> dict:
    with engine_manager.engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    return {
        "status": "ok",
        "dialect": engine_manager.engine.dialect.name,
        "driver": engine_manager.engine.dialect.driver,
    }
