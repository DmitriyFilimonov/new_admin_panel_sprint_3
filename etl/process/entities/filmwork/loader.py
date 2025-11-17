from datetime import datetime
from typing import Generator

from process.es_client import create_scheme, send_bulk
from state.state import State
from process.entities.models import FilmWorkESDoc, FilmWorkESDocRaw
from process.entities.filmwork.constants import STATE_KEY
from utils import coroutine


@coroutine
def load_movies_by_modified(
    state: State,
) -> Generator[None, list[FilmWorkESDocRaw], None]:
    while filworks := (yield):
        if state.get_state(state_key=STATE_KEY) == datetime.min:
            create_scheme()

        last_modified = filworks[-1].modified
        send_bulk(
            bulk=[
                FilmWorkESDoc(
                    actors=f.actors,
                    actors_names=f.actors_names,
                    description=f.description,
                    directors=f.directors,
                    directors_names=f.directors_names,
                    genres=f.genres,
                    id=f.id,
                    imdb_rating=f.imdb_rating,
                    title=f.title,
                    writers=f.writers,
                    writers_names=f.writers_names,
                )
                for f in filworks
            ]
        )
        print(last_modified, flush=True)
        state.set_state(state_key=STATE_KEY, value=last_modified)
