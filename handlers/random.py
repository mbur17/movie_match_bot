from typing import Union

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from .keyboards import get_movie_keyboard
from tmdb_api.tmdb import get_random_movie


# Функция отправки фильма
async def send_new_movie(request: Union[Message | CallbackQuery]):
    movie = await get_random_movie()
    genre_str = ', '.join(movie['genres']) if movie['genres'] else '-'
    rating_str = f'{movie["rating"]:.1f}' if movie['rating'] else '—'

    text = (
        f'<b>{movie["title"]}</b>\n\n'
        f'{movie["overview"]}\n\n'
        f'<b>Рейтинг:</b> {rating_str} / 10\n'
        f'<b>Жанры:</b> {genre_str}\n'
        f'<b>Дата выхода:</b> {movie["release_date"]}'
    )

    if movie['poster_url']:
        if isinstance(request, CallbackQuery):
            await request.message.answer_photo(
                photo=movie['poster_url'],
                caption=text,
                parse_mode='HTML',
                reply_markup=get_movie_keyboard()
            )
        else:
            await request.answer_photo(
                photo=movie['poster_url'],
                caption=text,
                parse_mode='HTML',
                reply_markup=get_movie_keyboard()
            )
    else:
        await request.answer(
            text, parse_mode='HTML', reply_markup=get_movie_keyboard()
        )

