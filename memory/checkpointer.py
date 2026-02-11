import os
from langgraph.checkpoint.postgres import PostgresSaver

_checkpointer = None
_cm = None

def get_checkpointer():
    global _checkpointer, _cm

    if _checkpointer is None:
        database_url = os.getenv("DATABASE_URL")

        # Create context manager ONCE
        _cm = PostgresSaver.from_conn_string(database_url)

        # Enter it ONCE and keep it alive
        _checkpointer = _cm.__enter__()
        _checkpointer.setup()

    return _checkpointer
