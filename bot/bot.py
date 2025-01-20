import asyncio
import logging
import json
from bot.middlewares.user_middleware import UserMiddleware
from bot.handlers.inline import router
from bot.callbacks.cross_zeroes_callBack import router as router_call_back
from bot.handlers.commands import router as c_r
from bot.handlers.messages import router as router_m
from bot.callbacks.menu_callback import router as router_mc 
from gameControll.game import game
from bot.bot_configs import bot, dp
from bot.contexts.wordlie_context import router as wr


async def main() -> None:
    dp.update.middleware(UserMiddleware())
    dp.include_routers(
        wr,
        router,
        c_r,
        router_mc,
        router_m,
        router_call_back
    )
    await bot.delete_webhook(True)
    with open("words.json", "r", encoding="UTF-8") as f:
        game.wordlie.words = json.load(f)
        f.close()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
    
