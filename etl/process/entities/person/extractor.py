from datetime import datetime
from psycopg import ServerCursor

from process.entities.dataclasses import FilmWork


def extract_movies_by_person_modified(pg_cursor: ServerCursor) -> list[FilmWork]:
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
                        'person_role', pfw_selection.role,
                        'person_id', p_selection.id,
                        'person_name', p_selection.full_name
                    )
                ) FILTER (WHERE p_selection.id is not null),
                '[]'
            ) as persons,
            array_agg(DISTINCT g.name) as genres
        FROM content.person p_filter
        JOIN content.person_film_work pfw_filter ON pfw_filter.person_id = p_filter.id
        JOIN content.film_work fw ON fw.id = pfw_filter.film_work_id
        
        LEFT JOIN content.person_film_work pfw_selection ON pfw_selection.film_work_id = fw.id
        LEFT JOIN content.person p_selection ON p_selection.id = pfw_selection.person_id
        
        LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
        LEFT JOIN content.genre g ON g.id = gfw.genre_id


        WHERE p_filter.modified > %s
        GROUP BY fw.id
        ORDER BY MAX(p_filter.modified)
        LIMIT 100;
        """,
        (datetime.min,),
    )

    filmworks_extended = pg_cursor.fetchall()

    return [FilmWork(**dict(filmwork)) for filmwork in filmworks_extended]
