from abc import ABC, abstractmethod

from aiogram import Bot, Router, F
from aiogram.types import CallbackQuery

from .random import send_new_movie


class BaseCallbackHandler(ABC):
    def __init__(self, bot: Bot):
        self.bot = bot

    @abstractmethod
    def register(self, router: Router):
        pass


class StartRandom(BaseCallbackHandler):
    def register(self, router: Router):
        router.callback_query.register(
            self.handle_start_random, F.data == 'start_random',

        )

    async def handle_start_random(self, callback: CallbackQuery):
        await send_new_movie(callback)


class LikeSkipStop(BaseCallbackHandler):
    def register(self, router: Router):
        router.callback_query.register(
            self.handle_buttons, F.data.in_({
                'like',
                'skip',
                'stop',

            }),

        )

    async def handle_buttons(self, callback: CallbackQuery):
        if callback.data == 'like':
            await callback.answer('Добавлено в избранное ✅')
            await send_new_movie(callback.message)

        elif callback.data == 'skip':
            await callback.answer('Пропускаем ⏭')
            await send_new_movie(callback.message)

        elif callback.data == 'stop':
            await callback.message.answer('Режим подбора завершён. Спасибо! 👋')
            await callback.answer()


class CallbacksHandler:
    def __init__(self, bot: Bot,):
        self.bot = bot
        self.router = Router()

        self.handlers = [
            StartRandom(self.bot),
            LikeSkipStop(self.bot),


        ]

        for handler in self.handlers:
            handler.register(self.router)
