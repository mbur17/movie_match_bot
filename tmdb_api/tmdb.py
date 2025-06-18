import logging
import random

import aiohttp
from async_lru import alru_cache

from config import TMDB_API_KEY

from .constants import (
    GENRE_LIST_ENDPOINT,
    HEADERS,
    LANGUAGE,
    MAX_ATTEMPTS,
    SEARCH_MOVIE_ENDPOINT
)

from .services import get_random_letter, get_random_year
from .validators import is_russian_text, is_valid_release_date

logger = logging.getLogger(__name__)


@alru_cache(maxsize=1)
async def get_genre_map():
    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        params = {
            'api_key': TMDB_API_KEY,
            'language': LANGUAGE
        }
        try:
            async with session.get(
                GENRE_LIST_ENDPOINT, params=params, headers=HEADERS
            ) as response:
                data = await response.json()
                return {
                    g['id']: g['name'] for g in data.get('genres', [])
                }
        except Exception as e:
            logger.warning(f'[TMDB] Ошибка запроса жанров: {e}')
            return {}


async def get_random_movie(attempt=1):
    if attempt > MAX_ATTEMPTS:
        raise Exception(
            'Не удалось найти подходящий фильм после нескольких попыток'
        )

    letter = get_random_letter()
    release_year = get_random_year()

    connector = aiohttp.TCPConnector(ssl=False)
    async with aiohttp.ClientSession(connector=connector) as session:
        # Первый запрос — получаем total_pages.
        params = {
            'api_key': TMDB_API_KEY,
            'language': LANGUAGE,
            'query': letter,
            'primary_release_year': release_year,
        }

        try:
            async with session.get(
                SEARCH_MOVIE_ENDPOINT, params=params, headers=HEADERS
            ) as response:
                data = await response.json()
                total_pages = min(data.get('total_pages', 1), 500)
                if total_pages == 0:
                    return await get_random_movie(attempt + 1)

            # Запрашиваем случайную страницу.
            params['page'] = random.randint(1, total_pages)
            async with session.get(
                SEARCH_MOVIE_ENDPOINT, params=params, headers=HEADERS
            ) as response:
                movies_data = await response.json()

        except Exception as e:
            logger.warning(f'[TMDB] Ошибка запроса на попытке {attempt}: {e}')
            return await get_random_movie(attempt + 1)

    candidates = movies_data.get('results', [])
    if not candidates:
        return await get_random_movie(attempt + 1)

    valid_movies = [
        m for m in candidates
        if is_valid_release_date(m.get('release_date')) and
        is_russian_text(m.get('title')) and
        is_russian_text(m.get('overview'))
    ]

    if not valid_movies:
        return await get_random_movie(attempt + 1)

    movie = random.choice(valid_movies)
    genre_map = await get_genre_map()
    genres = [
        genre_map.get(gid, '-') for gid in movie.get('genre_ids', [])
    ]

    return {
        'title': movie['title'],
        'overview': movie.get('overview', '-'),
        'release_date': movie['release_date'],
        'rating': movie.get('vote_average'),
        'genres': genres,
        'poster_url': (
            f'https://image.tmdb.org/t/p/w500{movie["poster_path"]}'
            if movie.get('poster_path') else None
        ),
    }


async def init_tmdb():
    genres = await get_genre_map()
    logger.info(f'[TMDB] Загружено жанров: {len(genres)}')
