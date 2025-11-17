from datetime import datetime
from time import sleep

from dsl import dsl

import psycopg
from psycopg import ServerCursor, connection as _connection
from psycopg.rows import class_row

from utils import backoff
from process.entities.filmwork.etl import movies_etl
from state.state import JsonFileStorage, State
from process.entities.dataclasses import FilmWork


@backoff(border_sleep_time=40)
def start_etl():
    with (
        psycopg.connect(**dsl, row_factory=class_row(FilmWork)) as connection,
        ServerCursor(connection=connection, name="loader") as cursor,
    ):
        storage = JsonFileStorage()
        state = State(storage)

        movies_etl(cursor=cursor, state=state)


if __name__ == "__main__":
    start_etl()
