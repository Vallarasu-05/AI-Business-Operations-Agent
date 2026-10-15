from app.config import settings


def get_checkpointer():
    """MemorySaver by default. Set USE_POSTGRES_CHECKPOINTER=true + DATABASE_URL for persistence."""
    if settings.use_postgres_checkpointer and settings.database_url.startswith("postgres"):
        from langgraph.checkpoint.postgres import PostgresSaver
        from psycopg import Connection
        conn = Connection.connect(settings.database_url.replace("+psycopg", ""), autocommit=True)
        saver = PostgresSaver(conn)
        saver.setup()
        return saver
    from langgraph.checkpoint.memory import MemorySaver
    return MemorySaver()
