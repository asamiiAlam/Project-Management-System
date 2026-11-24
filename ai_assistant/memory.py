import os
from langgraph.checkpoint.postgres import PostgresSaver


def get_checkpointer():
    return PostgresSaver.from_conn_string(
        os.environ["DATABASE_URL"]
    )