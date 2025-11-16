from datetime import datetime

from dsl import dsl

import psycopg
from psycopg import ClientCursor, connection as _connection
from psycopg.rows import dict_row

from process.entities.filmwork.extractor import extrract_movies_by_modified

if __name__ == "__main__":
    with psycopg.connect(
        **dsl, row_factory=dict_row, cursor_factory=ClientCursor
    ) as pg_conn:
        cursor = pg_conn.cursor(row_factory=dict_row)

        filmworks = extrract_movies_by_modified(cursor)

