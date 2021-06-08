import os

from databases import Database

__all__ = ['db']


def database_url():
    uid = os.getenv("POSTGRES_UID", "user")
    pwd = os.getenv("POSTGRES_PWD", "password")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = int(os.getenv("POSTGRES_PORT", 5432))

    return f"postgresql://{uid}:{pwd}@{host}:{port}/db"


db = Database(database_url())
