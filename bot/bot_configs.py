from aiogram import Bot, Dispatcher
from bot.config import settings

bot = Bot(settings.BOT_TOKEN.get_secret_value())
dp = Dispatcher()
print(dp)

async def get_state(bot, id) -> str:
    s = dp.fsm.get_context(
        bot,
        id,
        id
    )
    w = await s.get_data()
    return w["state"]
async def set_state(bot, id, state):
    s = dp.fsm.get_context(
        bot,
        id,
        id
    )
    await s.update_data(state=state)