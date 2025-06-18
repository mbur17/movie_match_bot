from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from .keyboards import get_movie_keyboard
from tmdb_api.tmdb import get_random_movie

router = Router()


# Хендлер команды /random
@router.message(Command('random'))
async def random_handler(message: Message):
    await send_new_movie(message)


# Функция отправки фильма
async def send_new_movie(target):
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
        await target.answer_photo(
            photo=movie['poster_url'],
            caption=text,
            parse_mode='HTML',
            reply_markup=get_movie_keyboard()
        )
    else:
        await target.answer(
            text, parse_mode='HTML', reply_markup=get_movie_keyboard()
        )


# Обработка нажатий на кнопки
@router.callback_query(F.data.in_({'like', 'skip', 'stop'}))
async def process_vote(callback: CallbackQuery):
    if callback.data == 'like':
        await callback.answer('Добавлено в избранное ✅')
        await send_new_movie(callback.message)

    elif callback.data == 'skip':
        await callback.answer('Пропускаем ⏭')
        await send_new_movie(callback.message)

    elif callback.data == 'stop':
        await callback.message.answer('Режим подбора завершён. Спасибо! 👋')
        await callback.answer()
