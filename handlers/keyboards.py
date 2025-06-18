from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_menu_keyboard():
    pass


def get_movie_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='✅ Буду смотреть', callback_data='like'),
            InlineKeyboardButton(text='⏭ Пропустить', callback_data='skip'),
        ],
        [
            InlineKeyboardButton(text='🛑 Завершить', callback_data='stop')
        ]
    ])
