import os

dsl = {
    "dbname": os.environ.get("POSTGRES_DB"),
    "user": os.environ.get("POSTGRES_USER"),
    "password": os.environ.get("POSTGRES_PASSWORD"),
    "host": os.environ.get("SQL_HOST"),
    "port": os.environ.get("SQL_PORT"),
}
