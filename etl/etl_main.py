from datetime import datetime

from dsl import dsl

import psycopg
from psycopg import ClientCursor, connection as _connection
from psycopg.rows import dict_row

from process.entities.person.extractor import extract_movies_by_person_modified
from process.entities.genre.extractor import extract_movies_by_genre_modified
from process.entities.filmwork.extractor import extract_movies_by_modified

if __name__ == "__main__":
    with psycopg.connect(
        **dsl, row_factory=dict_row, cursor_factory=ClientCursor
    ) as pg_conn:
        cursor = pg_conn.cursor(row_factory=dict_row)

        filmworks = extract_movies_by_modified(cursor)

        print(filmworks[0])

        filmworks = extract_movies_by_genre_modified(cursor)

        print(filmworks[0])

        filmworks = extract_movies_by_person_modified(cursor)

        print(filmworks[0])

