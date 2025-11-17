from datetime import datetime
from typing import Generator
from psycopg import ServerCursor

from utils import coroutine
from process.entities.models import FilmWork


@coroutine
def extract_movies_by_genre_modified(
    cursor: ServerCursor[FilmWork],
    next: Generator[None, list[FilmWork], None],
) -> Generator[None, datetime, None]:

    while last_updated := (yield):
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
            array_agg(DISTINCT g_selection.name) as genres
            FROM content.genre g_filter
            JOIN content.genre_film_work gfw_filter ON gfw_filter.genre_id = g_filter.id
            JOIN content.film_work fw ON fw.id = gfw_filter.film_work_id
            LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
            LEFT JOIN content.person p ON p.id = pfw.person_id

            LEFT JOIN content.genre_film_work gfw_selection ON gfw_selection.film_work_id = fw.id
            LEFT JOIN content.genre g_selection ON g_selection.id = gfw_selection.genre_id

            WHERE g_filter.modified > %s
            GROUP BY fw.id
            ORDER BY MAX(g_filter.modified)
            LIMIT 100;
            """,
            (last_updated,),
        )

        while results := cursor.fetchmany(size=100):
            next.send(results)
