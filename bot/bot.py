import asyncio
from aiogram import Bot, Dispatcher
import logging
from bot.config import settings
from bot.middlewares.user_middleware import UserMiddleware
from bot.handlers.inline import router
from bot.callbacks.cross_zeroes_callBack import router as router_call_back
from bot.handlers.commands import router as c_r
from bot.handlers.messages import router as router_m
from bot.callbacks.menu_callback import router as router_mc 

async def main() -> None:
    bot = Bot(settings.BOT_TOKEN.get_secret_value())
    dp = Dispatcher()
    dp.update.middleware(UserMiddleware())
    dp.include_routers(
        router,
        c_r,
        router_mc,
        router_m,
        router_call_back
    )
    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    #print()
    asyncio.run(main())
    
