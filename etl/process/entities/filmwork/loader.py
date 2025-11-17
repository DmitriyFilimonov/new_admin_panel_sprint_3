from datetime import datetime
from typing import Generator

from state.state import State
from process.entities.dataclasses import FilmWork
from process.entities.filmwork.constants import STATE_KEY
from utils import coroutine


@coroutine
def load_movies_by_modified(state: State) -> Generator[None, list[FilmWork], None]:
    while filworks := (yield):
        last_modified = filworks[-1].modified
        state.set_state(state_key=STATE_KEY, value=last_modified)
