from abc import ABC, abstractmethod

from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, Command
from aiogram.types import Message

from handlers.keyboards import Keyboards
from .random import send_new_movie

keyboard = Keyboards()


class BaseCommandHandler(ABC):
    def __init__(self, bot: Bot):
        self.bot = bot

    @abstractmethod
    def register(self, router: Router):
        pass


class StartCommandHandler(BaseCommandHandler):
    def register(self, router: Router):
        router.message.register(
            self.start_handler_private, CommandStart(), (F.chat.type == "private")
        )
        router.message.register(
            self.start_handler_group, CommandStart(), (F.chat.type == "group") | (F.chat.type == "supergroup")
        )

    async def start_handler_private(self, message: Message):
        await message.answer(
            'Привет! Думаешь что посмотреть? ...',
            reply_markup=keyboard.init,

        )

    async def start_handler_group(self, message: Message):
        await message.answer("Пока что только для чатов 1 на 1...")


class RandomCommandHandler(BaseCommandHandler):
    def register(self, router: Router):
        router.message.register(
            self.send_random_movie, Command("random"),

        )

    async def send_random_movie(self, message: Message):
        await send_new_movie(message)


class CommandsHandler:
    def __init__(self, tg_bot: Bot):
        self.bot = tg_bot
        self.router = Router()

        self._handlers = [
            StartCommandHandler(self.bot),
            RandomCommandHandler(self.bot),

        ]

        for handler in self._handlers:
            handler.register(self.router)
