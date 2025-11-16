from datetime import datetime
from psycopg import Cursor

from process.entities.dataclasses import FilmWork


def extrract_movies_by_modified(pg_cursor: Cursor) -> list[FilmWork]:
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
        (datetime.min,),
    )

    filmworks_extended = pg_cursor.fetchall()

    return [FilmWork(**dict(filmwork)) for filmwork in filmworks_extended]
