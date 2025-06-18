from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_menu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [

            ]
        ]
    )


def get_movie_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='✅ Буду смотреть', callback_data='like'),
                InlineKeyboardButton(text='⏭ Пропустить', callback_data='skip'),

            ],
            [
                InlineKeyboardButton(text='🛑 Завершить', callback_data='stop'),

            ]
        ]
    )


def get_init_keyboard():
    return InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='🎲 Случайный фильм', callback_data='start_random'),

                ],

            ]
    )


class Keyboards:
    def __init__(self):
        self.init = get_init_keyboard()
        self.menu = get_menu_keyboard()
        self.movie = get_movie_keyboard()

