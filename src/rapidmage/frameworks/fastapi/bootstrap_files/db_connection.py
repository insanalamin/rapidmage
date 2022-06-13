import sqlalchemy
from sqlalchemy.sql import text
import os

db_password = os.getenv('POSTGRES_PASSWORD', default=None)

engine = sqlalchemy.create_engine(
    "postgresql://postgres:{}@localhost:5441/postgres".format(db_password)
)


def db_execute(statement, payload):
    with engine.connect() as conn:
        result = conn.execute(text(statement), **payload)

        return result
