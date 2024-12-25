from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()
@router.callback_query(F.data == "cross_zeroes")
async def go_to_cross_zeroes(call: CallbackQuery):
    await call.message.answer("Игра против друга или рейтинг?")
    