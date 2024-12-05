import asyncio
from aiogram import Bot, Dispatcher
from commands import router
from controlGames import router_m
import logging



async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot("7121712678:AAFySaj9YeXAtUSPDJoXYDNTtb4CAZpS3AI")
    dp = Dispatcher()
    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
