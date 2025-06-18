from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import (
    CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
)

from .random import random_handler

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text='🎲 Случайный фильм', callback_data='start_random'
            )]
        ]
    )
    await message.answer(
        'Привет! Думаешь что посмотреть? ...',
        reply_markup=keyboard
    )


@router.callback_query(F.data == 'start_random')
async def handle_start_random(callback: CallbackQuery):
    await callback.answer()
    await random_handler(callback.message)
