from time import sleep
from psycopg import ServerCursor

from process.entities.models import FilmWork
from process.entities.filmwork.constants import STATE_KEY
from state.state import State
from process.entities.filmwork.extractor import extract_movies_by_modified
from process.entities.filmwork.transformer import transform_movies_by_modified
from process.entities.filmwork.loader import load_movies_by_modified


def movies_etl(cursor: ServerCursor[FilmWork], state: State):
    loader = load_movies_by_modified(state)
    transformer = transform_movies_by_modified(next=loader)
    extractor = extract_movies_by_modified(cursor=cursor, next=transformer)

    while True:
        last_update = state.get_state(STATE_KEY)

        extractor.send(last_update)

        sleep(15)
