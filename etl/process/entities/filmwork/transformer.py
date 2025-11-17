from typing import Generator

from process.entities.dataclasses import FilmWork

from utils import coroutine


@coroutine
def transform_movies_by_modified(
    next: Generator[None, list[FilmWork], None],
) -> Generator[None, list[FilmWork], None]:
    while filworks := (yield):
        for filwork in filworks:
            filwork.title = filwork.title.upper()

        transformed_filworks = filworks

        next.send(transformed_filworks)
