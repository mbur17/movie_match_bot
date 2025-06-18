import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import random_router, hello_router
from tmdb_api.tmdb import init_tmdb


async def main() -> None:
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    dp.include_router(hello_router)
    dp.include_router(random_router)

    await init_tmdb()
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
