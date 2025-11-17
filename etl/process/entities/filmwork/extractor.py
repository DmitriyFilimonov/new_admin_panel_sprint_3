from datetime import datetime
from typing import Generator

from utils import backoff, coroutine
from process.entities.dataclasses import FilmWork

import psycopg
from psycopg import ServerCursor

from dsl import dsl
from psycopg.rows import class_row


@backoff(border_sleep_time=40)
def get_pg_connection():
    return psycopg.connect(**dsl, row_factory=class_row(FilmWork))


@backoff(border_sleep_time=40)
def execute_wrapper(cursor: ServerCursor, last_updated: datetime):
    cursor.execute(
        """
            SELECT
            fw.id,
            fw.title,
            fw.description,
            fw.rating,
            fw.type,
            fw.created,
            fw.modified,
            COALESCE (
                json_agg(
                    DISTINCT jsonb_build_object(
                        'person_role', pfw.role,
                        'person_id', p.id,
                        'person_name', p.full_name
                    )
                ) FILTER (WHERE p.id is not null),
                '[]'
            ) as persons,
            array_agg(DISTINCT g.name) as genres
            FROM content.film_work fw
            LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
            LEFT JOIN content.person p ON p.id = pfw.person_id
            LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
            LEFT JOIN content.genre g ON g.id = gfw.genre_id
            WHERE fw.modified > %s
            GROUP BY fw.id
            ORDER BY fw.modified
            LIMIT 100;
            """,
        (last_updated,),
    )


@coroutine
def extract_movies_by_modified(
    next: Generator[None, list[FilmWork], None],
) -> Generator[None, datetime, None]:
    with (
        get_pg_connection() as connection,
        ServerCursor(connection=connection, name="extractor") as cursor,
    ):
        while last_updated := (yield):
            execute_wrapper(cursor=cursor, last_updated=last_updated)

            while results := cursor.fetchmany(size=100):
                next.send(results)
