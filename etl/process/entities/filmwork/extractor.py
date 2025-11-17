from datetime import datetime
from typing import Generator
from psycopg import ServerCursor

from utils import coroutine
from process.entities.dataclasses import FilmWork


@coroutine
def extract_movies_by_modified(
    pg_cursor: ServerCursor[FilmWork], next: Generator[None, list[FilmWork], None]
) -> Generator[None, datetime, None]:
    while last_updated := (yield):
        pg_cursor.execute(
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

        while results := pg_cursor.fetchmany(size=100):
            next.send(results)
