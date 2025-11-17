import psycopg
from utils import backoff
from process.entities.models import FilmWork
from process.entities.filmwork.etl import movies_etl
from state.state import JsonFileStorage, State
from psycopg.rows import class_row
from settings import settings


@backoff(border_sleep_time=60)
def start_etl():
    with (
        psycopg.connect(
            **settings.get_dsl(), row_factory=class_row(FilmWork)
        ) as connection,
        psycopg.ServerCursor(connection=connection, name="extractor") as cursor,
    ):
        storage = JsonFileStorage()
        state = State(storage)

        movies_etl(cursor=cursor, state=state)


if __name__ == "__main__":
    start_etl()
