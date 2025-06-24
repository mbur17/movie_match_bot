import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import commands_handler, callbacks_handler
from tmdb_api.tmdb import init_tmdb


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_routers(
        commands_handler(bot).router,
        callbacks_handler(bot).router,

    )

    await init_tmdb()
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
