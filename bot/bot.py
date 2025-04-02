import asyncio
import json
from .handlers import main_router_handler
from .middlewares.user_middleware import UserMiddleware 
from gameControll.game import game
from .bot_configs import bot, dp
from .contexts import main_router_contexts
from .callbacks import main_router_callback
from .logger import cl

async def main() -> None:
    dp.update.middleware(UserMiddleware())
    cl.schedule.start()
    game.mafia_schedule.start()
    cl.schedule.add_job(
        cl.send_logs_to_admin,
        trigger='cron',
        hour=00,
        minute=00,
        kwargs={"bot":bot}  # Укажите вашу временную зону
    )
    dp.include_routers(
        main_router_handler,
        main_router_callback,
        main_router_contexts,
    )
    await bot.delete_webhook(True)
    with open("words.json", "r", encoding="UTF-8") as f:
        game.wordlie.words = json.load(f)
        f.close()
    cl.custom_logger.debug("Бот запущен", extra={"username": "SYSTEM",
                                       "state": "nothing",
                                       "handler_name": "MAIN",
                                       "params":"nothing"})
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
    
