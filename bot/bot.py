import asyncio
from aiogram import Bot, Dispatcher
from commands import router
from controlGames import router_m
import logging
from config import settings
from middlewares import UserMiddleware


async def main() -> None:
    bot = Bot(settings.BOT_TOKEN.get_secret_value())
    dp = Dispatcher()
    dp.update.middleware(UserMiddleware())
    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
