from aiogram import Router, F
from aiogram.types import CallbackQuery
from gameControll.game import game
import logging

router = Router()

@router.callback_query(F.data.endswith('top'))
async def check_top(call: CallbackQuery):
    text = await game.get_top(call.data[:-4])
    await call.message.answer(text)
    logging.info(
                f"пользователь зашел в топ {call.data[:-4]}",
                    extra={"username": call.from_user.username,
                    "state": "nothing",
                    "handler_name": "get_top",
                    "params":"nothing"}
                    )